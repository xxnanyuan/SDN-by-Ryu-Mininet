# SDN-by-Ryu-Mininet
## timeline
- May 18 21:30 complete task 1 & 2 
- May 23 17:00 complete task 3
- May 24 22:00 complete load balance
- June 02 morning complete firewall

## environment
for python 3.9- version:
```
% pip3 install dnspython==1.16.0 eventlet==0.30.2 ryu=4.34.4
```
for all python version:
```
% pip3 install ryu
```
To install the dependent of latest ryu. But the version of ryu and eventlet is conflict, so you need to uninstall ryu and install it from the github repository:  
```
% pip3 uninstall ryu
% git clone https://github.com/faucetsdn/ryu.git
% cd ryu; pip3 install .
```

## structure of the project
### load balance part
- net_start.py: file to setup the basic mininet network.
* initial.txt: delay, bandwidth and loss of the network.
- LS_route.py: the main file to implement LS algorithm and a basic load balance.
- dijk.py: dijk algorithm and will be called in LS_router.
- routeWeight.py: compute the cost of all links by a function related to delay, bandwidth and loss.
- CallRestApi.py: Encapsulate rest api function.
### firewall
- task3.py
- firewall.py 

## Resource
### 刘星圆:
- https://www.cnblogs.com/ssyfj/p/11750559.html
- https://www.cnblogs.com/ssyfj/p/11762093.html
- [openflow流表组成](https://www.cnblogs.com/ssyfj/p/12573143.html)
- [openflow流表匹配](https://blog.csdn.net/lady_killer9/article/details/104540806)

### 陈奕锦:
- https://blog.csdn.net/lady_killer9/article/details/104559470
- https://github.com/faucetsdn/ryu/blob/master/ryu/app/ofctl_rest.py
- https://www.freesion.com/article/8090870623/
- https://osrg.github.io/ryu-book/en/html/rest_router.html
- https://osrg.github.io/ryu-book/en/html/rest_firewall.html

### xxnanyuan(waiting to detail):
- [source code of ryu](https://github.com/faucetsdn/ryu/tree/master/ryu) 
- [ryu book](https://book.ryu-sdn.org/en/html/)(notice that the traditional chinese version has some miss chapters)
- [ryu document](https://ryu.readthedocs.io/en/latest/) 

### 艾骥:
- [防火牆（ Firewall ） — Ryubook 1.0 說明文件](https://osrg.github.io/ryu-book/zh_tw/html/rest_firewall.html)
- [source code](https://github.com/faucetsdn/ryu/blob/master/ryu/app/rest_firewall.py)
- https://blog.csdn.net/qq_44807756/article/details/127915755
- http://pzengseu.github.io/2016/01/24/SDN/ryu-firewall/
