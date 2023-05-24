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
    print("LS_table: ",LS_table)
    return LS_table

# 下发流表
def send_flow_table(LS_table, output_port, priority=10000):
    for src in LS_table:
        for dst in LS_table[src]:
            if LS_table[src][dst]==-1:
                continue
            match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.add_flow_entry(src,match,priority,actions)
# delete流表
def delete_flow_table(LS_table, output_port, priority=10000):
    for src in LS_table:
        for dst in LS_table[src]:
            if LS_table[src][dst]==-1:
                continue
            match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.delete_flow_entry(src,match,priority,actions)

def get_p_bytes(dpids,net):
    p_bytes={}
    for dpid in dpids:
        p_bytes[dpid[-1]]={}
        for iterm in CallRestApi.get_flow_entries(dpid[-1])[dpid[-1]]:
            if iterm["priority"]==10000:
                if  net["s"+dpid[-1]+"-eth"+iterm["actions"][0][-1]][1] in p_bytes[dpid[-1]].keys():
                    p_bytes[dpid[-1]][net["s"+dpid[-1]+"-eth"+iterm["actions"][0][-1]][1]]=p_bytes[dpid[-1]][net["s"+dpid[-1]+"-eth"+iterm["actions"][0][-1]][1]]+iterm["byte_count"]
                else:
                    p_bytes[dpid[-1]][net["s"+dpid[-1]+"-eth"+iterm["actions"][0][-1]][1]]=iterm["byte_count"]

    for dpid1 in dpids:
        for dpid2 in dpids:
            if (dpid1!=dpid2):
                if dpid2[-1] not in p_bytes[dpid1[-1]].keys():
                    p_bytes[dpid1[-1]][dpid2[-1]]=0 
    return p_bytes

def get_used_bandwidth(dpids,net):
    p_bytes=get_p_bytes(dpids,net)
    bw=[]
    bw.append(p_bytes["1"]["2"]+p_bytes["2"]["1"])
    bw.append(p_bytes["1"]["3"]+p_bytes["3"]["1"])
    bw.append(p_bytes["2"]["3"]+p_bytes["3"]["2"])
    return bw,p_bytes

def init_flow_table():
    global last_flow_table
    dpids,switches=get_route_info()
    net,output_port=get_net_info()
    topo_graph=create_graph(dpids,net,[1,1,1])
    flow_table=calculate_flow_table(topo_graph)
    send_flow_table(flow_table,output_port,10000)
    last_flow_table=copy.deepcopy(flow_table)

init_flow_table()
# keep update    

def load_balance(dtime,net,output_port):
    global last_flow_table
    dpids,switches=get_route_info()
    bw,p_bytes=get_used_bandwidth(dpids,net)
    print("bw_input: ",bw[0]*800/(10e6)/dtime,bw[1]*800/(10e6)/dtime,bw[2]*800/(10e6)/dtime)
    cost=routeWeight.main(bw[0]*800/(10e6)/dtime,bw[1]*800/(10e6)/dtime,bw[2]*800/(10e6)/dtime)
    topo_graph=create_graph(dpids,net,cost)
    flow_table=calculate_flow_table(topo_graph)
    delete_flow_table(last_flow_table,output_port,10000)
    send_flow_table(flow_table,output_port,10000)
    last_flow_table=copy.deepcopy(flow_table)

    
last_time=time.time()
while True:
    net,output_port=get_net_info()
    cost=[1,1,1]
    if (net!=last_net):
        dpids,switches=get_route_info()
        last_net=copy.deepcopy(net)
        topo_graph=create_graph(dpids,net,cost)
        flow_table=calculate_flow_table(topo_graph)
        send_flow_table(flow_table,output_port,10000)
    if (time.time()-last_time>=10):
        dtime=time.time()-last_time
        last_time=time.time()
        load_balance(dtime,net,output_port)

