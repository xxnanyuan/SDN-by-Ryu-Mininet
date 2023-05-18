from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController


net = Mininet(controller=RemoteController) # 创建 Mininet 实例，指定控制器类型为 RemoteController
hosts = [net.addHost(f'h{i + 1}', ip=f'223.1.{i + 1}.2/24')
         for i in range(3)] # 创建三个主机，分别设置 IP 地址
switches = [net.addSwitch(f's{i + 1}') for i in range(3)] # 创建三个交换机
c0 = net.addController('c0') # 添加控制器

net.addLink(switches[0], hosts[0])
net.addLink(switches[1], hosts[1])
net.addLink(switches[2], hosts[2]) # 将主机和交换机连接
net.addLink(switches[0], switches[1])
net.addLink(switches[1], switches[2])
net.addLink(switches[2], switches[0])# 将交换机之间连接成环状拓扑

net.start() net.start() # 启动网络


c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.1.1/24"}' http://localhost:8080/router/0000000000000001 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.4.1/24"}' http://localhost:8080/router/0000000000000001 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.6.2/24"}' http://localhost:8080/router/0000000000000001 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.2.1/24"}' http://localhost:8080/router/0000000000000002 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.4.2/24"}' http://localhost:8080/router/0000000000000002 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.5.1/24"}' http://localhost:8080/router/0000000000000002 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.3.1/24"}' http://localhost:8080/router/0000000000000003 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.5.2/24"}' http://localhost:8080/router/0000000000000003 ''')
c0.cmd(
    ''' curl -X POST -d '{"address": "223.1.6.1/24"}' http://localhost:8080/router/0000000000000003 ''')

for i in range(3):
    hosts[i].cmd(f'ip route add default via 223.1.{i + 1}.1')

# set defalut routes 默认路由
c0.cmd('''curl -X POST -d '{"gateway": "223.1.4.2"}' http://localhost:8080/router/0000000000000001''')
c0.cmd('''curl -X POST -d '{"gateway": "223.1.5.2"}' http://localhost:8080/router/0000000000000002''')
c0.cmd('''curl -X POST -d '{"gateway": "223.1.6.2"}' http://localhost:8080/router/0000000000000003''')
# 对于默认路由，每个路由器分别设置了不同的网关地址：223.1.4.2、223.1.5.2和223.1.6.2

# set static routes 静态路由
c0.cmd('''curl -X POST -d '{"destination": "223.1.3.0/24", "gateway": "223.1.6.1"}' http://localhost:8080/router/0000000000000001''')   
c0.cmd('''curl -X POST -d '{"destination": "223.1.1.0/24", "gateway": "223.1.4.1"}' http://localhost:8080/router/0000000000000002''')   
c0.cmd('''curl -X POST -d '{"destination": "223.1.2.0/24", "gateway": "223.1.5.1"}' http://localhost:8080/router/0000000000000003''')

# 对于静态路由，目标网络和对应的网关地址:
# 路由器0000000000000001：目标网络223.1.3.0/24，网关地址为223.1.6.1
# 路由器0000000000000002：目标网络223.1.1.0/24，网关地址为223.1.4.1
# 路由器0000000000000003：目标网络223.1.2.0/24，网关地址为223.1.5.1

CLI(net) # 启动Mininet的命令行界面，允许用户在模拟网络环境中执行命令

net.stop()
