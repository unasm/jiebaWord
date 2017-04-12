# -*- coding:utf-8 -*- 

import networkx as nx
import matplotlib.pyplot as plt  
from networkx.algorithms import approximation as approx
import json
import math
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite import json_graph
from networkx.utils import powerlaw_sequence
#print powerlaw_sequence
#z = nx.utils.create_degree_sequence(5, powerlaw_sequence)
#G = nx.configuration_model(z)

#G = nx.Graph()
#G = nx.balanced_tree(2, 4)
#G = nx.wheel_graph(20)
#G = nx.grid_2d_graph(3, 3)
#G = nx.dorogovtsev_goltsev_mendes_graph(3)
#G = nx.barbell_graph(4, 3)
#G = nx.barbell_graph(4, 3)
#print nx.barbell_graph()
#G = nx.star_graph(20)
#G = nx.make_small_graph(["adjacencylist","C_4",4,[[2,4],[3],[4],[]]])
#G=nx.make_small_graph(["edgelist","C_4",4,[[1,2],[3,1],[2,3],[4,1]]])

#G=nx.frucht_graph()
#G=nx.chvatal_graph()
#G=nx.bull_graph()
#print G.labels()
#label = draw_networkx_labels(G, )

#G=nx.dodecahedral_graph()
G=nx.petersen_graph()
#G=nx.diamond_graph()
#G=nx.desargues_graph()
#G=nx.LCF_graph(24, [12, 7, -7], 8)
#pos = nx.spring_layout(G)
#nx.draw_networkx_labels(G,pos)

#G=nx.LCF_graph(16, [5,-5], 8)
#G=nx.icosahedral_graph()
#G=nx.house_x_graph()
#G=nx.geographical_threshold_graph(10, 0.3)
#G=nx.ego_graph(G, 3)
#print nx.fiedler_vector(G)
#G=nx.random_geometric_graph(20, 0.3)
#G = nx.lollipop_graph(4, 8)
#G = nx.grid_graph(dim = [3, 3])
#G.add_edge('y', 'x', function=math.cos)
#G.add_node(math.cos)
##G.add_node(1)
##G.add_node(2)
##G.add_node(3)
##G.add_edge(1, 2)
#nx.draw_networkx(G)
#nx.draw_graphviz(G)
#nx.draw_shell(G)

print nx.all_pairs_node_connectivity(G)

#data = json_graph.node_link_data(G)
#print type(data)
#s = json.dumps(data)
#print type(s)
nx.draw(G, with_labels = True)
#nx.draw_circular(G, with_labels = True)
#nx.draw_circular(G, with_labels = True, cmap = plt.cm.Blues, node_color=range(len(G)), style = "dotted")
#pos = nx.spring_layout(G)
#nx.draw_spring(G, with_labels = True)
#nx.draw_spectral(G, with_labels = True)
plt.show()
