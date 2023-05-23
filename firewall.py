# 在需要使用防火墙功能的文件顶部添加引入语句
# from firewall import add_firewall_rule_block_ip, add_firewall_rule_block_destination, add_firewall_rule_block_keyword


# 添加防火墙规则
# add_firewall_rule_block_ip("0000000000000001", "10.0.0.1")
# add_firewall_rule_block_destination("0000000000000002", "10.0.0.2")
# add_firewall_rule_block_keyword("0000000000000003", "hack")

# 启动 ryu-magager ryu.app.rest_firewall ryu.app.ofctl_rest ryu.app.rest_topology ryu.app.ws_topology --observe-links

# 防火墙规则成功添加后print消息比如 Adding firewall rule to block packets containing keyword 'hack'

# 测试防火墙规则生效情况：
# 1.是否阻止来自 某主机ip 的数据包
# 2.是否阻止试图访问 某主机ip 的数据包
#     1.新开一个终端窗口
#     2.连接到mn网络中的主机 
#     mnexec -a mn -- bash -c 'ip netns exec h1 bash' h1主机的网络命名空间
#     3.使用ping 命令 ping 10.0.0.2
# 是否阻止来自h1 主机ip 10.0.0.1的数据包
# 是否阻止试图访问 h2 主机ip10.0.0.2的数据包
# 预期返回：destination host unreachable或者请求超时

# 3.自定义字段的数据包
# scapy或 hping 来构造自定义的数据包，并尝试发送包含关键字 "hack" 的数据包到目标主机 有问题


import requests

# 下发流表规则


def install_flow_rule(switch_id, match_fields, actions):
    url = f"http://localhost:8080/stats/flowentry/add"
    data = {
        "switch": switch_id,
        "priority": 200,  # 为了确保防火墙规则优先级高于负载均衡规则，设置较高的优先级
        "match": match_fields,
        "actions": actions
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

# 防火墙规则：拒绝来自某 IP 地址的数据包


def add_firewall_rule_block_ip(switch_id, ip_address):
    match_fields = {
        "ipv4_src": ip_address
    }
    actions = []
    success = install_flow_rule(switch_id, match_fields, actions)
    if success:
        print(f"Firewall rule added to block packets from {ip_address}")
    else:
        print(
            f"Failed to add firewall rule to block packets from {ip_address}")

# 防火墙规则：拒绝试图访问某个主机的数据包


def add_firewall_rule_block_destination(switch_id, destination_ip):
    match_fields = {
        "ipv4_dst": destination_ip
    }
    actions = []
    success = install_flow_rule(switch_id, match_fields, actions)
    if success:
        print(f"Firewall rule added to block packets to {destination_ip}")
    else:
        print(
            f"Failed to add firewall rule to block packets to {destination_ip}")

# 防火墙规则：禁止包含某些关键字的数据包


def add_firewall_rule_block_keyword(switch_id, keyword):
    match_fields = {
        "tcp_payload": keyword
    }
    actions = []
    success = install_flow_rule(switch_id, match_fields, actions)
    if success:
        print(
            f"Firewall rule added to block packets containing keyword '{keyword}'")
    else:
        print(
            f"Failed to add firewall rule to block packets containing keyword '{keyword}'")


# 获取交换机ID和对应的流量统计数据
switches = {"0000000000000001": "223.1.1.1/24",
            "0000000000000002": "223.1.2.1/24", "0000000000000003": "223.1.3.1/24"}



# 运行SDN网络
# ...
