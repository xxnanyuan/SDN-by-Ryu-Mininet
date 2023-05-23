'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-05-20 23:09:55
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-05-23 16:25:46
FilePath: \project\SDN-by-Ryu-Mininet-master\CallRestApi.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 此文件将rest api的调用封装起来
# 关于rest api的具体情况请参考https://github.com/faucetsdn/ryu/blob/master/ryu/app文件夹下ofctl_rest.py、rest_router.py、rest_topology.py
import requests 
import json

# 获取所有交换机信息
def get_all_switches():
    url = "http://127.0.0.1:8080/v1.0/topology/switches"
    req = requests.get(url).json()
    return req
   
# 获取所有链路信息 
def get_all_links():
    url = "http://127.0.0.1:8080/v1.0/topology/links"
    req = requests.get(url).json()
    return req
   
# 获取dpid为dpid（可以理解为交换机序号）的交换机的所有流表，此处dpid不为16位
def get_flow_entries(dpid):
    url = "http://127.0.0.1:8080/stats/flow/" + dpid
    req = requests.get(url).json()
    return req
   
# 给dpid为dpid（可以理解为交换机序号）的交换机添加一个流表项，
# 关于流表项的具体设置：
# priority默认设置为1000
# match中目的地ip设置应为一个子网中所有ip，即1.0.0.0/24，最后一位为0（参照http://osrg.github.io/ryu-book/en/html/rest_router.html），其他项请自行查阅文档
# actions的设置：action主要有两种，一是output，附带端口，二是drop，即丢包
# 此处dpid不为16位
def add_flow_entry(dpid,match,priority,actions):
    url = "http://127.0.0.1:8080/stats/flowentry/add"
    post_data = "{'dpid':%s,'match':%s,'priority':%s,'actions':%s}" % (dpid,str(match),priority,str(actions))
    req = requests.post(url,data=post_data)
    return req.status_code
   
# 删除一个流表项
# 本项目中用不到
def delete_flow_entry(dpid, match=None, priority=None, actions=None):
    url = "http://127.0.0.1:8080/stats/flowentry/delete"
    post_data = "{'dpid':%s" % dpid
    if match is not None:
        post_data += ",'match':%s" % str(match)
    if priority is not None:
        post_data += ",'priority':%s" % priority
    if actions is not None:
        post_data += ",'actions':%s" % str(actions)
    post_data += "}"
    req = requests.post(url,data=post_data)
    return req.getcode()

# 获取路由信息
def get_router(dpid):
    url = "http://localhost:8080/router/"+dpid
    req = requests.get(url).json()
    return req

#修改路由信息
def modify_flow_entry(dpid,match,priority,actions):
    url = "http://127.0.0.1:8080/stats/flowentry/modify"
    post_data = "{'dpid':%s,'match':%s,'priority':%s,'actions':%s}" % (dpid,str(match),priority,str(actions))
    req = requests.post(url,data=post_data)
    return req.status_code
