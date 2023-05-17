import requests 
import json
 
def get_all_switches():
    url = "http://127.0.0.1:8080/v1.0/topology/switches"
    req = requests.get(url).json()
    return req
 
def get_all_links():
    url = "http://127.0.0.1:8080/v1.0/topology/links"
    req = requests.get(url).json()
    return req
 
def get_switch(dpid):
    url = "http://127.0.0.1:8080/v1.0/topology/switches/" + dpid
    req = requests.get(url).json()
    return req
 
def get_flow_entries(dpid):
    url = "http://127.0.0.1:8080/stats/flow/" + dpid
    req = requests.get(url).json()
    return req
 
def add_flow_entry(dpid,match,priority,actions):
    url = "http://127.0.0.1:8080/stats/flowentry/add"
    post_data = "{'dpid':%s,'match':%s,'priority':%s,'actions':%s}" % (dpid,str(match),priority,str(actions))
    req = requests.post(url,data=post_data)
    print(post_data) 
    return req.status_code
 
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
    print(post_data) 
    req = requests.post(url,data=post_data)
    return res.getcode()

match1={"in_port":1,"nw_src":"223.1.1.2/24","nw_dst":"223.1.2.2/24","dl_type":2048}
priority=1000
actions1=[{"type":"OUTPUT","port":2}]

match2={"in_port":2,"nw_src":"223.1.1.2/24","nw_dst":"223.1.2.2/24","dl_type":2048}
priority=1000
actions2=[{"type":"OUTPUT","port":1}]

match3={"in_port":1,"nw_src":"223.1.2.2/24","nw_dst":"223.1.1.2/24","dl_type":2048}
priority=1000
actions3=[{"type":"OUTPUT","port":2}]

match4={"in_port":2,"nw_src":"223.1.2.2/24","nw_dst":"223.1.1.2/24","dl_type":2048}
priority=3000
actions4=[{"type":"OUTPUT","port":1}]

add_flow_entry("1",match1,priority,actions1)
#add_flow_entry("2",match2,priority,actions2)
#add_flow_entry("1",match3,priority,actions3)
#add_flow_entry("2",match4,priority,actions4)
