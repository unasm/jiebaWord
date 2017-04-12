# -*- coding:utf-8 -*- 
import networkx as nx
import random
import matplotlib.pyplot as plt  

G=nx.fast_gnp_random_graph(15,0.1)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
#nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()
