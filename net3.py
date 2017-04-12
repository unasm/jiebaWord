# -*- coding:utf-8 -*- 
import networkx as nx
import matplotlib.pyplot as plt  

G = nx.Graph(day = "Friday")
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_node("spam")
G.add_edge(1, 3)

for data in G.nodes():
    print data
#nx.draw(G)
nx.draw_networkx(G)
#nx.draw_networkx_nodes(G,pos)
#nx.draw_networkx_labels(G,pos)
#nx.draw_networkx_edges(G,pos)
#nx.draw_spectral(G,  with_labels=True)
#nx.draw(G)
plt.show()
