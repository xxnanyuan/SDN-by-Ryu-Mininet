import CallRestApi
from dijk import dijk_g
# 开启
# 先net_start.py以及LS_route.py，再 mininet 里测试 ping 录屏https://jbox.sjtu.edu.cn/v/link/view/b85156d213134d39b0159bb9ed9cea6f

# 防火墙和入侵检测功能
# 规则1 拒绝来自 h1（IP 地址为 223.1.1.2）的数据包
# 规则2 拒绝发送到 h1（IP 地址为 223.1.1.2）的数据包
# 规则3 拒绝传输层协议为 TCP、载荷包含 hack 的数据包

# 通过调用 CallRestApi，先得到网络拓扑和交换机信息
switches = {}
net = {}
output_port = {}
dpids = []




for switch in CallRestApi.get_all_switches():
    router = CallRestApi.get_router(switch["dpid"])
    dpids.append(switch["dpid"])
    switches[switch["dpid"]] = {port["name"]: router[0]["internal_network"][0]["address"][int(
        port["name"][-1])-1]["address"] for port in switch["ports"]}


for item in CallRestApi.get_all_links():
    net[item["src"]["name"]] = item["dst"]["name"]
    output_port[item["src"]["name"][1]+item["dst"]
                ["name"][1]] = int(item["src"]["name"][-1])

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

    match = {"nw_dst": "223.1.1.2", "dl_type": 2048}  # 拒绝发送到h1的数据包
    actions = []
    CallRestApi.add_flow_entry(src, match, 1000, actions)

    match = {"dl_type": 2048, "nw_proto": 6, "tcp_payload": "hack"}
    actions = []
    CallRestApi.add_flow_entry(src, match, 1000, actions)   # 拒绝TCP 载荷包含关键字 "hack"的数据包

  # 匹配协议类型为 IPv4（"dl_type": 2048）
  # 传输层协议类型为 TCP（"nw_proto": 6）
  # 三个防火墙规则

