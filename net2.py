# -*- coding:utf-8 -*- 
import networkx as nx
import matplotlib.pyplot as plt  

#G = nx.complete_graph(8)
G = nx.Graph(day = "Friday")
G.add_node(1, time = '5pm')
G.add_nodes_from([3], time = '2pm')
G.node[1]['room'] = 714
G.add_edge(1, 2, weight = 4.7)
G.add_edges_from([(3,4), (4, 5)], color = "red")
G[1][2]['weight'] = 4.7
nx.draw_networkx_labels(G)
plt.show()
