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

from hierarchicalQueryPython.graphCommon import readCiscoDataGraph


#plot graph functions here;  plot locally with matplotlib; plot in D3...
class visualizeDynamic(object):
    
    def __init__(self):
        pass
    
    
    #main entry visualize matplotlib
    def funcMainEntrySubgraphVisualizePlot(self):
        '''
        from a sub list ofnodes to get the subgraph
        then show with matplotlib
        '''
        
        ciscoNodeInfoFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphNodeInfo"
        ciscoAdjacentListFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphAdjacencyList"
    
        G = readCiscoDataGraph(ciscoAdjacentListFile, ciscoNodeInfoFile)
        candidatesNodeIdLst = [1,3,4,10]
        self.subgraphVisualizePlot(G, candidatesNodeIdLst)
    
    #main entry visualize in d3 js
    def funcMainEntrySubgraphVisualizeD3(self):
        '''
        from a sub list ofnodes to get the subgraph
        then show in D3.js
        '''
                
        ciscoNodeInfoFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphNodeInfo"
        ciscoAdjacentListFile = "/home/fubao/workDir/ResearchProjects/hierarchicalNetworkQuery/inputData/ciscoProductVulnerability/newCiscoGraphAdjacencyList"
    
        G = readCiscoDataGraph(ciscoAdjacentListFile, ciscoNodeInfoFile)
        outJsonFile = "outputPlot/subgraph.json"
        candidatesNodeIdLst = [1,3,4,10]
        self.subgraphVisualizeD3(G, candidatesNodeIdLst, outJsonFile)


    #visualize in d3 js
    def subgraphVisualizeD3(self, G, candidatesNodeIdLst, outJsonFile):
    
        #get nodes and edge to create a new graph
        newG = nx.MultiDiGraph()           #nx.DiGraph() 
    

        for nodeId in candidatesNodeIdLst:
            nodeType = G.node[nodeId]['labelType']
            nodeName = G.node[nodeId]['labelName']
            newG.add_node(nodeId, labelType=nodeType, labelName=nodeName)
            neighbors = G.neighbors(nodeId)
            for nb in neighbors:
                #key = G[nodeId][nb]["key"]
                newG.add_edge(nodeId, nb)
                nodeType = G.node[nb]['labelType']
                nodeName = G.node[nb]['labelName']
                newG.add_node(nb, labelType=nodeType, labelName=nodeName)
        
        #print node and edge sizes
        print ('438 drawtopKRelatedGraph node and edge sizes: ', len(G), G.size(), len(newG), newG.size())
        self.saveToJson(newG, outJsonFile)
        webbrowser.get('firefox').open_new_tab('index2.html')  
                
    #draw subgraph network nx 
    def subgraphVisualizePlot(self, G, candidatesNodeIdLst):
    
        g = nx.Graph()           #nx.DiGraph() 
        edges = G.edges(candidatesNodeIdLst)
        print ('edges3: ', edges, len(G[1]))
        for eg in edges:
            node0 = eg[0]
            node1 = eg[1]
            #g.add_node(node0, labelName = G.node[node0]['labelName'])
            #g.add_node(node1, labelName = G.node[node1]['labelName'])
            g.add_node(node0, labelName = str(node0))
            g.add_node(node1, labelName = str(node1))

            g.add_edge(eg[0], eg[1])
        pos = nx.spring_layout(g)
        #A = [3]
        #noCor = ["b" if n in A else "r" for n in G.nodes()]
        nx.draw(g, pos=pos, with_labels = True, labels =nx.get_node_attributes(g,'labelName'))   # labels =nx.get_node_attributes(G,'labelName'))
        #nx.draw_networkx_edges(G,pos=pos, edgelist = edges, node_color='b')
        #h = G.subgraph(A)
        #nx.draw_networkx_nodes(h,pos=pos, node_color=noCor) #or even nx.draw(h,pos=pos,node_color='b') to get nodes and edges in one command
        #nx.draw_networkx_edges(h,pos=pos)
        plt.savefig('graph.pdf')

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
                            G.node[u]['labelName'], G.node[v]['labelName'])} for u,v in G.edges()]),
                  open(fname, 'w'), indent=2)
        '''    
        
        #use nodeId as node label info to draw node 
        json.dump(dict(links=[{"source":u, "target":v, "value":(G.node[u]['labelType'], G.node[v]['labelType'], 
                            u,v)} for u,v in G.edges()]),
                  open(fname, 'w'), indent=2)
        
        
    def drawTestGraphOnline(self, G, outJsonFile):
        #test read
        adjacentListFile = "/home/fubao/Desktop/workDir/personalizedQuery/personalizedQuery_Drug/DataPrep/PersonalizedQueryPython/input/small_graph_adjacentList.txt"
        G = readTestGraph(adjacentListFile)
        saveToJson(G, outJsonFile)
        
        


    
    
if __name__ == "__main__":
    visualizeDynObj = visualizeDynamic()
    #visualizeDynObj.funcMainEntrySubgraphVisualizePlot()
    
    visualizeDynObj.funcMainEntrySubgraphVisualizeD3()
    