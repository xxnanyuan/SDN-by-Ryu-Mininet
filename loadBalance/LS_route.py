import time
import CallRestApi
from dijk import dijk_g
import routeWeight
import copy
# while true和time.sleep(5)结构配合使得每5秒计算一次静态路由，发送给交换机
last_net={}
# 下面通过调用rest api获取相关信息
def get_route_info():
    dpids=[]
    switches={}
    for switch in CallRestApi.get_all_switches():
        router=CallRestApi.get_router(switch["dpid"])
        dpids.append(switch["dpid"])
        switches[switch["dpid"]]={port["name"]:router[0]["internal_network"][0]["address"][int(port["name"][-1])-1]["address"] for port in switch["ports"]}
    return dpids, switches

def get_net_info():
    net={}
    output_port={}
    for item in CallRestApi.get_all_links():
        net[item["src"]["name"]]=item["dst"]["name"]
        output_port[item["src"]["name"][1]+item["dst"]["name"][1]]=int(item["src"]["name"][-1])
    return net, output_port

# 创建进入dijk中的图
def create_graph(dpids,net,cost):
    topo_graph={}
    for dpid in dpids:
        topo_graph[dpid[-1]]={}
    for edge in net:
        topo_graph[edge[1]][net[edge][1]]=cost[int(edge[1])+int(net[edge][1])-3]
    return topo_graph


# 调用LS算法，计算流表
def calculate_flow_table(topo_graph):
    LS_table=dijk_g(topo_graph)
    print(LS_table)
    return LS_table

# 下发流表
def send_flow_table(LS_table, output_port):
    for src in LS_table:
        for dst in LS_table[src]:
            if LS_table[src][dst]==-1:
                continue
            match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.add_flow_entry(src,match,10000,actions)

def init_flow_table():
    dpids,switches=get_route_info()
    net,output_port=get_net_info()
    last_net=copy.deepcopy(net)
    topo_graph=create_graph(dpids,net,[1,1,1])
    flow_table=calculate_flow_table(topo_graph)
    send_flow_table(flow_table,output_port)


init_flow_table()

def get_p_bytes(dpids,net):
    p_bytes={}
    for dpid in dpids:
        p_bytes[dpid[-1]]={net["s"+dpid[-1]+"-eth"+iterm["actions"][0][-1]][1]:iterm["byte_count"] for iterm in CallRestApi.get_flow_entries(dpid[-1])[dpid[-1]] if iterm["priority"]==10000}
    return p_bytes

def get_used_bandwidth(dpids,last_bytes,net):
    p_bytes=get_p_bytes(dpids,net)
    bw=[]
    bw.append(p_bytes["1"]["2"]+p_bytes["2"]["1"]-last_bytes["1"]["2"]-last_bytes["2"]["1"])
    bw.append(p_bytes["1"]["3"]+p_bytes["3"]["1"]-last_bytes["1"]["3"]-last_bytes["3"]["1"])
    bw.append(p_bytes["2"]["3"]+p_bytes["3"]["2"]-last_bytes["2"]["3"]-last_bytes["3"]["2"])

    return bw,p_bytes

last_time=time.time()
# keep update    
while True:
    net,output_port=get_net_info()
    cost=[1,1,1]
    if (net!=last_net):
        dpids,switches=get_route_info()
        last_net=copy.deepcopy(net)
        topo_graph=create_graph(dpids,net,cost)
        flow_table=calculate_flow_table(topo_graph)
        send_flow_table(flow_table,output_port)
    last_bytes=get_p_bytes(dpids,net)
    bw,now_bytes=get_used_bandwidth(dpids,last_bytes,net)
    if (time.time()-last_time>=2):
        if (last_bytes==now_bytes):
            continue
        last_bytes=copy.deepcopy(now_bytes)
        cost=routeWeight.main(bw[0]*8/(10e6),bw[1]*8/(10e6),bw[2]*8/(10e6))
        dpids,switches=get_route_info()
        topo_graph=create_graph(dpids,net,cost)
        print(topo_graph)
        flow_table=calculate_flow_table(topo_graph)
        send_flow_table(flow_table,output_port)
