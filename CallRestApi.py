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
 
def get_flow_entries(dpid):
    url = "http://127.0.0.1:8080/stats/flow/" + dpid
    req = requests.get(url).json()
    return req
 
def add_flow_entry(dpid,match,priority,actions):
    url = "http://127.0.0.1:8080/stats/flowentry/add"
    post_data = "{'dpid':%s,'match':%s,'priority':%s,'actions':%s}" % (dpid,str(match),priority,str(actions))
    req = requests.post(url,data=post_data)
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
    req = requests.post(url,data=post_data)
    return req.getcode()

def get_router(dpid):
    url = "http://localhost:8080/router/"+dpid
    req = requests.get(url).json()
    return req
#add_flow_entry("2",match4,priority,actions4)
