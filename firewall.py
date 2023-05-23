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

# 添加防火墙规则
add_firewall_rule_block_ip("0000000000000001", "10.0.0.1")
add_firewall_rule_block_destination("0000000000000002", "10.0.0.2")
add_firewall_rule_block_keyword("0000000000000003", "hack")

# 运行SDN网络
# ...
