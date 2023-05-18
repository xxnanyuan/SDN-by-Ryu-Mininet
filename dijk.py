#只需要看main函数和图g的储存方式，所有接口都写在上面
#这里只能支持输入数字，在python中获得链路信息的方法为：


# links = net.links
# for link in links:
#     print(link.intf1.name, link.intf2.name) intf1是src，intf2是dst，输出例子为 s1-eth2 s2-eth2
#
#我的想法是在源python文件中获得所有链路信息，然后我们把s1这种和图中的点一一对应。这里想法之后再聊，我想把
#同一个路由器的不同网卡之间的距离设置成0. 
#最后返回的路径也是用数字的，还需要再对应回去
#
#








class Dijkstra:
    def __init__(self, graph, start, goal):
        self.graph = graph      # 邻接表
        self.start = start      # 起点
        self.goal = goal        # 终点

        self.open_list = {}     # open 表
        self.closed_list = {}   # closed 表

        self.open_list[start] = 0.0     # 将起点放入 open_list 中

        self.parent = {start: None}     # 存储节点的父子关系。键为子节点，值为父节点。方便做最后路径的回溯
        self.min_dis = None             # 最短路径的长度

    def shortest_path(self):

        while True:
            if self.open_list is None:
                break
            distance, min_node = min(zip(self.open_list.values(), self.open_list.keys()))      # 取出距离最小的节点
            self.open_list.pop(min_node)                                                       # 将其从 open_list 中去除

            self.closed_list[min_node] = distance                  # 将节点加入 closed_list 中

            if min_node == self.goal:                              # 如果节点为终点
                self.min_dis = distance
                shortest_path = [self.goal]                        # 记录从终点回溯的路径
                father_node = self.parent[self.goal]
                while father_node != self.start:
                    shortest_path.append(father_node)
                    father_node = self.parent[father_node]
                shortest_path.append(self.start)
                return shortest_path[::-1]# 返回最短路径和最短路径长度

            for node in self.graph[min_node].keys():               # 遍历当前节点的邻接节点
                if node not in self.closed_list.keys():            # 邻接节点不在 closed_list 中
                    if node in self.open_list.keys():              # 如果节点在 open_list 中
                        if self.graph[min_node][node] + distance < self.open_list[node]:
                            self.open_list[node] = distance + self.graph[min_node][node]         # 更新节点的值
                            self.parent[node] = min_node           # 更新继承关系
                    else:                                          # 如果节点不在 open_list 中
                        self.open_list[node] = distance + self.graph[min_node][node]             # 计算节点的值，并加入 open_list 中
                        self.parent[node] = min_node               # 更新继承关系


    
# 将dijk封装起来，输入为一个二维字典，代表着网络链路的结构图，dict[src][dst]=cost，
# src为发出路由，dst为目的路由，cost为这条边的花费，因为以跳数为花费，cost默认为1
# 输出为一个二维字典字典dict[src][dst]=src_next，即从src到达dst的最短路径中src下一个节点是是什么，路由器据此将网络封包转发到那里
# comment by xxnanyuan
def dijk_g(g):
    next_node={}
    size=len(g)
    
    for i in g:
        next_node[i]={}
        for j in g:
            if i!=j:
                try:
                    dijk = Dijkstra(g, i, j)
                    next_node[i][j]=dijk.shortest_path()[1]
                except:
                    next_node[i][j]=-1

    return next_node
