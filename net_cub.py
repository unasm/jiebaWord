import networkx as nx
import matplotlib.pyplot as plt  
G = nx.cubical_graph()

print G[1]
print len(G.nodes())
print ""
print nx.info(G, 1)
print nx.density(G)
#nx.draw(G,pos=nx.spectral_layout(G), nodecolor='r',edge_color='b')
#plt.show()
