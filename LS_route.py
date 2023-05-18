import time
import CallRestApi
from dijk import dijk_g
while True:
    switches={}
    net={}
    output_port={}
    dpids=[]
    for switch in CallRestApi.get_all_switches():
        router=CallRestApi.get_router(switch["dpid"])
        dpids.append(switch["dpid"])
        switches[switch["dpid"]]={port["name"]:router[0]["internal_network"][0]["address"][int(port["name"][-1])-1]["address"] for port in switch["ports"]}
    for item in CallRestApi.get_all_links():
        net[item["src"]["name"]]=item["dst"]["name"]
        output_port[item["src"]["name"][1]+item["dst"]["name"][1]]=int(item["src"]["name"][-1])
    print(net)

    cost=1
    topo_graph={}
    for dpid in dpids:
        topo_graph[dpid[-1]]={}
    for edge in net:
        topo_graph[edge[1]][net[edge][1]]=cost

    LS_table=dijk_g(topo_graph)
    print(LS_table)
    for src in LS_table:
        for dst in LS_table[src]:
            match={"nw_dst":"223.1.%s.0/24"%dst,"dl_type":2048}
            actions=[{"type":"OUTPUT","port":int(output_port[src+LS_table[src][dst]])}]
            CallRestApi.add_flow_entry(src,match,1000,actions)
    time.sleep(5)
        
