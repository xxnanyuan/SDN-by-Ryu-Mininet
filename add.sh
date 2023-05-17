curl -X POST -d '{
	"dpid":"1",
    "priority": 2000,
    "flags": 1,
	"match":{
		"VLAN_ID":100,
		"IP_DST":"223.1.2.2/24",
		"in_port":1
	},
	"actions":[{"type":"OUTPUT","port":2}]
}' http://127.0.0.1:8080/stats/flowentry/add

curl -X POST -d '{
	"dpid":"1",
    "priority": 2000,
    "flags": 1,
	"match":{
		"VLAN_ID":100,
		"IP_DST":"223.1.1.2/24",
		"in_port":2
	},
	"actions":[{"type":"OUTPUT","port":1}]
}' http://127.0.0.1:8080/stats/flowentry/add

curl -X POST -d '{
	"dpid":"2",
    "priority": 2000,
    "flags": 1,
	"match":{
		"VLAN_ID":100,
		"IP_DST":"223.1.2.2/24",
		"in_port":1
	},
	"actions":[{"type":"OUTPUT","port":2}]
}' http://127.0.0.1:8080/stats/flowentry/add

curl -X POST -d '{
	"dpid":"2",
    "priority": 2000,
    "flags": 1,
	"match":{
		"VLAN_ID":100,
		"IP_DST":"223.1.1.2/24",
		"in_port":2
	},
	"actions":[{"type":"OUTPUT","port":1}]
}' http://127.0.0.1:8080/stats/flowentry/add
