from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController


net = Mininet(controller=RemoteController)
hosts = [net.addHost(f'h{i + 1}', ip=f'223.1.{i + 1}.2/24')
         for i in range(3)]
switches = [net.addSwitch(f's{i + 1}') for i in range(3)]
c0 = net.addController('c0')

net.addLink(switches[0], hosts[0], 1, 1)
net.addLink(switches[1], hosts[1], 1, 1)
net.addLink(switches[2], hosts[2], 1, 1)
net.addLink(switches[0], switches[1], 2, 2)
net.addLink(switches[1], switches[2], 3, 2)
net.addLink(switches[2], switches[0], 3, 3)

switches[0].cmd('ifconfig s1-eth1 0')
switches[0].cmd('ip addr add 223.1.1.1/24 brd + dev s1-eth1')
switches[0].cmd('ifconfig s1-eth2 0')
switches[0].cmd('ip addr add 223.1.4.1/24 brd + dev s1-eth2')
switches[0].cmd('ifconfig s1-eth3 0')
switches[0].cmd('ip addr add 223.1.6.2/24 brd + dev s1-eth3')

switches[1].cmd('ifconfig s2-eth1 0')
switches[1].cmd('ip addr add 223.1.2.1/24 brd + dev s2-eth1')
switches[1].cmd('ifconfig s2-eth2 0')
switches[1].cmd('ip addr add 223.1.4.2/24 brd + dev s2-eth2')
switches[1].cmd('ifconfig s2-eth3 0')
switches[1].cmd('ip addr add 223.1.5.1/24 brd + dev s2-eth3')

switches[2].cmd('ifconfig s3-eth1 0')
switches[2].cmd('ip addr add 223.1.3.1/24 brd + dev s3-eth1')
switches[2].cmd('ifconfig s3-eth2 0')
switches[2].cmd('ip addr add 223.1.5.2/24 brd + dev s3-eth2')
switches[2].cmd('ifconfig s3-eth3 0')
switches[2].cmd('ip addr add 223.1.6.1/24 brd + dev s3-eth3')

net.start()

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

CLI(net)

net.stop()
