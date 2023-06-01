import CallRestApi
from dijk import dijk_g
# 开启
# 先net_start.py以及LS_route.py，mininet 里测试 ping

# 防火墙和入侵检测功能
# 规则1 拒绝来自 h1（IP 地址为 223.1.1.2）的数据包
# 规则2 拒绝发送到 h2（IP 地址为 223.1.1.3）的数据包
# 规则3 拒绝传输层协议为 TCP、载荷包含hack 的数据包

switches = {}
net = {}
output_port = {}
dpids = []


# 调用rest api s_1, s_2, s_3
for switch in CallRestApi.get_all_switches():
    router = CallRestApi.get_router(switch["dpid"])
    dpids.append(switch["dpid"])
    switches[switch["dpid"]] = {port["name"]: router[0]["internal_network"][0]["address"][int(
        port["name"][-1])-1]["address"] for port in switch["ports"]}
# 获取switch和router的信息，存在 switches 字典

for item in CallRestApi.get_all_links():
    net[item["src"]["name"]] = item["dst"]["name"]
    output_port[item["src"]["name"][1]+item["dst"]
                ["name"][1]] = int(item["src"]["name"][-1])
# 获取了链路信息，存在 net 字典

cst = 1
topo_graph = {}
for dpid in dpids:
    topo_graph[dpid[-1]] = {}
for edge in net:
    topo_graph[edge[1]][net[edge][1]] = cst

# 拓扑图构建 LS_table
LS_table = dijk_g(topo_graph)


for src in LS_table:

    match = {"nw_src": "223.1.1.2", "dl_type": 2048}  # 拒绝来自h1的数据包
    actions = []
    CallRestApi.add_flow_entry(src, match, 1000, actions)

    match = {"nw_dst": "223.1.1.3", "dl_type": 2048}  # 拒绝发送到h2的数据包
    actions = []
    CallRestApi.add_flow_entry(src, match, 1000, actions)

    match = {"dl_type": 2048, "nw_proto": 6, "tcp_payload": "hack"}
    actions = []
    CallRestApi.add_flow_entry(src, match, 1000, actions)

  # 匹配协议类型为 IPv4（"dl_type": 2048）
  # 传输层协议类型为 TCP（"nw_proto": 6）
  # 三个防火墙规则
  # TCP 载荷包含关键字 "hack"
