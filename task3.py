'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-05-22 14:09:24
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-05-23 16:22:22
FilePath: \project\SDN-by-Ryu-Mininet-master\task3.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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
        print("Switch:",switch)
        router=CallRestApi.get_router(switch["dpid"])
        print("Router:",router)
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
            if LS_table[src][dst]==-1:
                continue
            if(int(dst)==2):
               #只允许TCP流量发送到h2
               match = {"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048,"nw_proto":6}
            else:
              match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.add_flow_entry(src,match,1000,actions)
    
    #h2发出的流量全部发往h1
    match={"nw_dst":"223.1.3.0/24","dl_type":2048}
    actions=[{"type":"SET_FIELD","field":"ipv4_dst","value":"223.1.1.2"},{"type":"OUTPUT","port":2}]
    CallRestApi.modify_flow_entry(str(2),match,2000,actions)
    
    time.sleep(5)
        
