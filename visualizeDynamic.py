#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:45:20 2017

@author: fubao
"""
import networkx as nx
import collections

import matplotlib.pyplot as plt
from networkx.readwrite import json_graph;
import json
import webbrowser
import sys
sys.path.append("../")

from hierarchicalQueryPython.graphCommon import readCiscoDataGraph, readTestGraph, readEdgeListToGraph


#plot graph functions here;  plot locally with matplotlib; plot in D3...
class visualizeDynamic(object):
    
    def __init__(self):
        pass
    
    
    #main entry visualize matplotlib
    def funcMainEntrySubgraphVisualizePlotCisoProductGraph(self):
        '''
        from a sub list ofnodes to get the subgraph from cisco data graph
        then show with matplotlib
        '''
        
        ciscoNodeInfoFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphNodeInfo"
        ciscoAdjacentListFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphAdjacencyList"
    
        G = readCiscoDataGraph(ciscoAdjacentListFile, ciscoNodeInfoFile)
        candidatesNodeIdLst = [1,3,4,10]
        
        self.subgraphVisualizePlot(G, candidatesNodeIdLst)
    
    #main entry visualize in d3 js
    def funcMainEntrySubgraphVisualizeD3CisoProductGraph(self):
        '''
        from a sub list ofnodes to get the subgraph from cisco data graph
        then show in D3.js
        '''
                
        ciscoNodeInfoFile = "../inputData/ciscoProductVulnerability/newCiscoGraphNodeInfo"
        ciscoAdjacentListFile = "../inputData/ciscoProductVulnerability/newCiscoGraphAdjacencyList"
    
        G = readCiscoDataGraph(ciscoAdjacentListFile, ciscoNodeInfoFile)
        outJsonFile = "outputPlot/subgraphCisco.json"
        candidatesNodeIdLst = [1,3,4,10]
        self.subgraphVisualizeD3(G, candidatesNodeIdLst, outJsonFile)


    #main entry visualize matplotlib
    def funcMainEntrySubgraphVisualizePlotSyntheticGraph(self):
        '''
        from a sub list ofnodes to get the subgraph from synthetic data graph
        then show with matplotlib
        '''
        syntheticGraphNodeInfoFile = "../../GraphQuerySearchRelatedPractice/Data/syntheticGraph/syntheticGraph_hierarchiRandom/syntheticGraphNodeInfo.tsv"
        syntheticGraphEdgeListFile = "../../GraphQuerySearchRelatedPractice/Data/syntheticGraph/syntheticGraph_hierarchiRandom/syntheticGraphEdgeListInfo.tsv"
    
        G = readEdgeListToGraph(syntheticGraphEdgeListFile, syntheticGraphNodeInfoFile)
        #candidatesNodeIdLst = [648027, 636461,8150, 28487, 72908, 16117, 16118]
        candidatesNodeIdLst = [3002]

        self.subgraphVisualizePlot(G, candidatesNodeIdLst)
        
        
    #main entry visualize in d3 js
    def funcMainEntrySubgraphVisualizeD3SyntheticGraph(self):
        '''
        from a sub list ofnodes to get the subgraph from synthetic data graph
        then show in D3.js
        '''
        syntheticGraphNodeInfoFile = "../../GraphQuerySearchRelatedPractice/Data/syntheticGraph/syntheticGraph_hierarchiRandom/syntheticGraphNodeInfo.tsv"
        syntheticGraphEdgeListFile = "../../GraphQuerySearchRelatedPractice/Data/syntheticGraph/syntheticGraph_hierarchiRandom/syntheticGraphEdgeListInfo.tsv"
    
        G = readEdgeListToGraph(syntheticGraphEdgeListFile, syntheticGraphNodeInfoFile)
        #outJsonFile = "outputPlot/subgraphSyntheticGraph.json"

        outJsonFile = "outputPlot/subgraphSyntheticGraphPath.json"
        specificNodesLst = [648027, 636461]
        candidatesNodesLst = [72908, 16118, 260271, 145344, 295663, 83026, 250077, 44531, 191184, 31959]
        #candidatesNodesLst = [8150, 28487, 72908, 16117, 16118]
        #candidatesNodeIdLst = [648027, 636461, 8150, 28487, 72908, 16117, 16118]
        #candidatesNodeIdLst = [648027, 636461]
        #self.subgraphVisualizeD3(G, specificNodesLst + candidatesNodesLst, outJsonFile)
        self.subgraphVisualizeD3Paths(G, specificNodesLst, candidatesNodesLst, outJsonFile)

    #visualize in d3 js
    def subgraphVisualizeD3NodeNeighbor(self, G, candidatesNodeIdLst, outJsonFile):
        '''
        visualize node and its neighbors
        '''
        #get nodes and edge to create a new graph
        newG = nx.MultiDiGraph()           #nx.DiGraph() 
            
        for nodeId in candidatesNodeIdLst:
            nodeType = G.node[nodeId]['labelType']
            nodeName = G.node[nodeId]['labelName']
            newG.add_node(nodeId, labelType=nodeType, labelName=nodeName)
            neighbors = G.neighbors(nodeId)
            for nb in neighbors:
                #key = G[nodeId][nb]["key"]
                newG.add_edge(nodeId, nb, key='hier', edgeHierDistance = G[nodeId][nb]['hierarchy']['edgeHierDistance'])
                #newG.add_edge(nb, nodeId, h = G[nb][nodeId]['hierarchy']['edgeHierDistance'])
                nodeType = G.node[nb]['labelType']
                nodeName = G.node[nb]['labelName']
                newG.add_node(nb, labelType=nodeType, labelName=nodeName)
        
        #print node and edge sizes
        print (' subgraphVisualizeD3NodeNeighbor node and edge sizes: ', len(G), G.size(), len(newG), newG.size())
        self.saveToJson(newG, outJsonFile)
        webbrowser.get('firefox').open_new_tab('plotIndex.html')  
    
    def subgraphVisualizeD3Paths(self, G, specificNodesLst, candidatesNodeIdLst, outJsonFile):
        '''
        visualize the shortest path from specificNodesLst to candidatesNodeIdLst
        '''
         #get nodes and edge to create a new graph
        newG = nx.MultiDiGraph()           #nx.DiGraph()
        for srcId in specificNodesLst:
            #nodeType = G.node[srcId]['labelType']
            #nodeName = G.node[srcId]['labelName']
            #newG.add_node(srcId, labelType=nodeType, labelName=nodeName)
            for dstId in candidatesNodeIdLst:
                #get all shortest paths in [srcId, dstId]
                shortestPathLst = [p for p in nx.all_shortest_paths(G,source=srcId,target=dstId)]   # nx.all_shortest_paths(G, srcId, dstId)
                print ('subgraphVisualizeD3Paths:', srcId, dstId, shortestPathLst)
                #get nodes
                for onePath in shortestPathLst:
                    prevNd = onePath[0]
                    for nd in onePath:
                        newG.add_node(nd, labelType=G.node[nd]['labelType'], labelName=G.node[nd]['labelName'])
                        #construct the edge along the path
                        if prevNd != nd:
                            newG.add_edge(prevNd, nd, key='hier', edgeHierDistance = G[prevNd][nd]['hierarchy']['edgeHierDistance'])
                        prevNd = nd
           #print node and edge sizes
        print ('subgraphVisualizeD3Paths node and edge sizes: ', len(G), G.size(), len(newG), newG.size())
        self.saveToJson(newG, outJsonFile)
        webbrowser.get('firefox').open_new_tab('plotIndex.html')       
                    
    #draw subgraph network nx 
    def subgraphVisualizePlot(self, G, candidatesNodeIdLst):
    
        g = nx.MultiDiGraph()               #  nx.Graph()  #nx.DiGraph() 
        edges = G.edges(candidatesNodeIdLst)
        #print ('edges3: ', edges, len(G[1]))
        for eg in edges:
            node0 = eg[0]
            node1 = eg[1]
            #g.add_node(node0, labelName = G.node[node0]['labelName'])
            #g.add_node(node1, labelName = G.node[node1]['labelName'])
            g.add_node(node0, labelName = str(node0)+"_" + str(G.node[node0]['labelType']))
            g.add_node(node1, labelName = str(node1)+"_" + str(G.node[node1]['labelType']))

            g.add_edge(eg[0], eg[1], h = G[eg[0]][eg[1]]['hierarchy']['edgeHierDistance'])            # 'h' is the hierarchical level distance edge
        pos = nx.spring_layout(g)
        #A = [3]
        #noCor = ["b" if n in A else "r" for n in G.nodes()]
        colorMap = [G.node[nd]['labelType'] for nd in g.nodes()]
        #nx.draw(g, pos=pos, with_labels = True, node_color = colorMap, width= 2, labels =nx.get_node_attributes(g,'labelName'))   # labels =nx.get_node_attributes(G,'labelName'))
        nx.draw(g, pos, node_color = colorMap)
        nx.draw_networkx_labels(g, pos,  labels = nx.get_node_attributes(g,'labelName'))
        nx.draw_networkx_edge_labels(g, pos, labels = nx.get_edge_attributes(g,'h'))

        #nx.draw_networkx_edges(g, pos=pos,  node_color= colorMap,  labels =nx.get_node_attributes(g,'labelName'))
        #h = G.subgraph(A)
        #nx.draw_networkx_nodes(h,pos=pos, node_color=noCor) #or even nx.draw(h,pos=pos,node_color='b') to get nodes and edges in one command
        #nx.draw_networkx_edges(h,pos=pos)
        plt.savefig('outputPlot/subgraph.pdf')
        plt.show()


    #draw degree histrogram of graph
    def drawDegree(self, G):
        #G = nx.gnp_random_graph(100, 0.02)
        #average degree
        
        averDegree = sum(G.degree().values())/len(G.degree())
        print ('average degree: ', averDegree, G.number_of_edges())
        degree_sequence=sorted([d for n,d in G.degree().items()], reverse=True) # degree sequence
        #print ("Degree sequence", degree_sequence)
        degreeCount=collections.Counter(degree_sequence)
        deg, cnt = zip(*degreeCount.items())
        
        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color='b')
        
        plt.title("Degree Histogram")
        plt.ylabel("Count")
        plt.xlabel("Degree")
        ax.set_xticks([d+0.4 for d in deg])
        ax.set_xticklabels(deg)
        
    
    #save to Json first, then use javascript (in .html) to call json 
    def saveToJson(self, G, fname):        
        #use label info (name etc) to draw node 
        
        '''
        json.dump(dict(links=[{"source":u, "target":v, "value":(G.node[u]['labelType'], G.node[v]['labelType'], 
                            G.node[u]['labelName'], G.node[v]['labelName'], G[u][v]['hier']['edgeHierDistance'])} for u,v in G.edges()]),
                  open(fname, 'w'), indent=2)
       
    
        '''
        '''
        #use nodeId as node label info to draw node 
        json.dump(dict(links=[{"source":u, "target":v, "value":(G.node[u]['labelType'], G.node[v]['labelType'], 
                            u,v, G[u][v]['hier']['edgeHierDistance'])} for u,v in G.edges()]),
                  open(fname, 'w'), indent=2)
        '''
        
        json.dump(dict(links=[{"source":u, "target":v, "src_type":G.node[u]['labelType'], "dst_type": G.node[v]['labelType'], "src_name":G.node[u]['labelName'], "dst_name":G.node[v]['labelName'], "edge_hier": (str(u) + "->" + str(v) + ": " + str(G[u][v]['hier']['edgeHierDistance']))} for u,v in G.edges()]),
                  open(fname, 'w'), indent=2)

        
        
    def drawTestGraphOnline(self, G, outJsonFile):
        #test read
        adjacentListFile = "/home/fubao/Desktop/workDir/personalizedQuery/personalizedQuery_Drug/DataPrep/PersonalizedQueryPython/input/small_graph_adjacentList.txt"
        G = readTestGraph(adjacentListFile)
        self.saveToJson(G, outJsonFile)
        
        
    
    
if __name__ == "__main__":
    visualizeDynObj = visualizeDynamic()
    #visualizeDynObj.funcMainEntrySubgraphVisualizePlot()
    
    #visualizeDynObj.funcMainEntrySubgraphVisualizeD3CisoProductGraph()
    
    #visualizeDynObj.funcMainEntrySubgraphVisualizePlotSyntheticGraph()
    visualizeDynObj.funcMainEntrySubgraphVisualizeD3SyntheticGraph()
