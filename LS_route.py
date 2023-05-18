import time
import CallRestApi
from dijk import dijk_g
# while true和time.sleep(5)结构配合使得每5秒计算一次静态路由，发送给交换机
while True:
    switches={} # 交换机信息
    net={} # 链路结构信息
    output_port={} # 转发规则，以"12":2为例，从1直接发送到2的封包通过1的第2个网卡发出
    dpids=[]
    
    # 下面通过调用rest api获取相关信息
    for switch in CallRestApi.get_all_switches():
        router=CallRestApi.get_router(switch["dpid"])
        dpids.append(switch["dpid"])
        switches[switch["dpid"]]={port["name"]:router[0]["internal_network"][0]["address"][int(port["name"][-1])-1]["address"] for port in switch["ports"]}
    for item in CallRestApi.get_all_links():
        net[item["src"]["name"]]=item["dst"]["name"]
        output_port[item["src"]["name"][1]+item["dst"]["name"][1]]=int(item["src"]["name"][-1])
    print(net)
    
    # 创建进入dijk中的图
    cost=1
    topo_graph={}
    for dpid in dpids:
        topo_graph[dpid[-1]]={}
    for edge in net:
        topo_graph[edge[1]][net[edge][1]]=cost
    
    # 调用LS算法，计算流表
    LS_table=dijk_g(topo_graph)
    print(LS_table)
    
    # 下发流表
    for src in LS_table:
        for dst in LS_table[src]:
            match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.add_flow_entry(src,match,1000,actions)
    time.sleep(5)
        
