curl -X POST -d '{
"dpid":"1",
"match":{
	"nw_src":"223.1.1.2/24",
	"nw_dst":"223.1.2.2/24",
	"in_port":1
},
"actions":[{"type":"OUTPUT","port":2}]
}' http://127.0.0.1:8080/stats/flowentry/add
