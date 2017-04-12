# -*- coding:utf-8 -*- 
import networkx as nx
import random
import matplotlib.pyplot as plt  

G = nx.path_graph(5)

nx.set_edge_attributes(G, 'my_weight', dict(zip(G.edges(), [random.random()*10 for edge in G.edges()])))
pos = nx.spring_layout(G, weight='my_weight')
nx.draw(G, pos)
plt.show()
