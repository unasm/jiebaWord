import matplotlib.pyplot as plt  
import sys
import numpy as np
import networkx as nx
from collections import defaultdict
#from networkx.algorithms import approximation as apxa

d = [['a',0],['a',1],['a',2],['b',1],['b',2],['c',1],['c',2],['c',3],['d',2],['d',3], ['e',0],['e',4],['f',0],['f',4],['g',0],['g',4],['g',5],['h',0],['h',5],['i',6]]

def constructFlowNetwork (C):
    E = defaultdict(lambda:0)
    E[('source',C[0][1])] += 1
    E[(C[-1][1],'sink')] += 1
    F = zip(C[:-1],C[1:])
    for i in F:
        if i[0][0]==i[1][0]:
            E[(i[0][1],i[1][1])]+=1
        else:
            E[(i[0][1],'sink')]+=1
    #G = nx.DiGraph()
    G = nx.DiGraph(day = "Friday", name = "my graph")
    for i,j in E.items():
        x, y = i
        print x, y, j
        G.add_edge(x, y, weight = j)
    return G

def getFlowMatrix(G,nodelist=None):
    if nodelist is None:
        FM = nx.to_numpy_matrix(G)
    FM = nx.to_numpy_matrix(G,nodelist)
    return FM


def getMarkovMatrix(m):
    '''
        read flowMatrix and construct MarkovMatrix      
    '''
    n = len(m)
    mm = np.zeros((n,n),np.float)
    for i in range(n):
        for j in range(n):
            if m[i,j]>0:
                mm[i,j] = float(m[i,j])/float((m[i,0:].sum()))
    return mm
G = constructFlowNetwork(d)
matrix = getFlowMatrix(G)
print matrix
print getMarkovMatrix(matrix)
#G = nx.Graph()
#G = nx.DiGraph()
#nx.draw(G, pos = nx.nx_agraph.graphviz_layout(G), cmap=plt.cm.Blues, node_color=range(len(G)), with_labels=True)
#nx.draw(G)
#plt.show()
