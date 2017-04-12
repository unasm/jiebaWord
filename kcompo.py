import matplotlib.pyplot as plt  
import sys
import networkx as nx
from networkx.algorithms import approximation as apxa


#print sys.argv[1]
userMap = {}
idxToUser = {}
cnt = 0
tradeMap = {}
tradeMapRev = {}
tradeCnt = {}
for line in open(sys.argv[1]):
    lineArr = line.strip().split()
    if not userMap.has_key(lineArr[1]):
        userMap[lineArr[1]] = cnt
        idxToUser[cnt] = lineArr[1]
        #print lineArr[1],cnt
        cnt += 1 
    if not userMap.has_key(lineArr[2]):
        idxToUser[cnt] = lineArr[2]
        userMap[lineArr[2]] = cnt
        #print lineArr[2], cnt
        cnt += 1 
    if not tradeMap.has_key(lineArr[1]):
        tradeMap[lineArr[1]] = {}
    if not tradeMapRev.has_key(lineArr[2]):
        tradeMapRev[lineArr[2]] = {}

    if not tradeMap[lineArr[1]].has_key(lineArr[2]):
        tradeMap[lineArr[1]][lineArr[2]] = {"times":0, "amount" : 0}
    if not tradeMapRev[lineArr[2]].has_key(lineArr[1]):
        tradeMapRev[lineArr[2]][lineArr[1]] = {"times":0, "amount" : 0}

    tradeMap[lineArr[1]][lineArr[2]]['times'] += 1 
    tradeMap[lineArr[1]][lineArr[2]]['amount'] += float(lineArr[3]) 

    tradeMapRev[lineArr[2]][lineArr[1]]['amount'] += float(lineArr[3])
    tradeMapRev[lineArr[2]][lineArr[1]]['times'] += 1


def getUndirGraph(path):
    G = nx.Graph()
    # make undirect graph
    for line in open(path):
        lineArr = line.strip().split()
        G.add_edge(userMap[lineArr[1]], userMap[lineArr[2]])
    return G

def getLimit(minVal, maxVal, compList):
    #a
    dbSet = set()
    #dbSet = list()
    for val in comps:
        if len(val) > minVal and len(val) < maxVal:
        #if len(val) > 200 and len(val) < 400:
            dbSet = val
            break
    return dbSet
def getDiGraph(dbSet):
    dG = nx.DiGraph(day = "Friday", name = "my graph")
    #dG.add_node(27, {"color":"blue"})
    for fromUser in dbSet:
        #print idxToUser[val]
        if tradeMap.has_key(idxToUser[fromUser]):
            #print tradeMap[idxToUser[val]]
            #print len(tradeMap[idxToUser[val]])
            for to in tradeMap[idxToUser[fromUser]]:
                node = tradeMap[idxToUser[fromUser]][to]
                dG.add_edges_from([(fromUser, userMap[to], {'weight' : node['times'], 'color' : 'blue'})])
    return dG
            #print fromUser,"-->", userMap[to]
G = getUndirGraph(sys.argv[1])
print "to calcuate max_cliet"
print apxa.maximum_independent_set(G)
#print apxa.average_clustering(G)
#print apxa.max_clique(G)
#print len(apxa.max_clique(G))
#comps = nx.connected_components(G)
#dbSet = getLimit(100, 200, comps)
#dbSet = getLimit(200, 400, comps)
#dG = getDiGraph(dbSet)
#print apxa.node_connectivity(dG)
#nx.draw_circular(dG)
#nxPos = nx.nx_agraph.graphviz_layout(dG, prog = 'dot')
#print nxPos
#nx.draw(dG, pos = nx.nx_agraph.graphviz_layout(dG), cmap=plt.cm.Blues, node_color=range(len(dG)))
#nx.draw_spectral(dG)
#nx.draw_networkx(dG)
#plt.show()
#print dG.graph
