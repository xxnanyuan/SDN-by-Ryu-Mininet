from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
import json


initial = []

with open ("initial.txt", "r")as f:
    lst = f.read()
print(lst)
tmp = json.loads(lst)
print(tmp)
for i in tmp.values():
    initial.append(i)

#带宽 时延 丢包率

net = Mininet(controller=RemoteController)
hosts = [net.addHost(f'h{i + 1}', ip=f'223.1.{i + 1}.2/24')
         for i in range(3)]
switches = [net.addSwitch(f's{i + 1}') for i in range(3)]
c0 = net.addController('c0')

net.addLink(switches[0], hosts[0])
net.addLink(switches[1], hosts[1])
net.addLink(switches[2], hosts[2])
net.addLink(switches[0], switches[1], bw = initial[0][0] , delay =f'{initial[0][1]}ms' , loss =initial[0][2] )
net.addLink(switches[1], switches[2], bw = initial[2][0], delay =f'{initial[2][1]}ms' , loss =initial[2][2])
net.addLink(switches[2], switches[0], bw = initial[1][0], delay =f'{initial[1][1]}ms' , loss =initial[1][2])

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

#c0.cmd('''curl -X POST -d '{"gateway": "223.1.4.2"}' http://localhost:8080/router/0000000000000001''')
#c0.cmd('''curl -X POST -d '{"gateway": "223.1.5.2"}' http://localhost:8080/router/0000000000000002''')
#c0.cmd('''curl -X POST -d '{"gateway": "223.1.6.2"}' http://localhost:8080/router/0000000000000003''')
#c0.cmd('''curl -X POST -d '{"destination": "223.1.3.0/24", "gateway": "223.1.6.1"}' http://localhost:8080/router/0000000000000001''')   
#c0.cmd('''curl -X POST -d '{"destination": "223.1.1.0/24", "gateway": "223.1.4.1"}' http://localhost:8080/router/0000000000000002''')   
#c0.cmd('''curl -X POST -d '{"destination": "223.1.2.0/24", "gateway": "223.1.5.1"}' http://localhost:8080/router/0000000000000003''')   
for i in range(3):
    hosts[i].cmd(f'ip route add default via 223.1.{i + 1}.1')

CLI(net)

net.stop()
