from ast import For
from ctypes import sizeof
from xmlrpc.client import Boolean
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os
from data_structures import InputStructure
from data_structures import OutputStructure



def Draw_Picture(Input: InputStructure, Output: OutputStructure, WithOld: Boolean = False):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)
    
    FNAMEO = GNNPICOUT + '/' + Input.Fname + '_O.png'
    FNAMEA = GNNPICOUT + '/' + Input.Fname + '_A.png'

    if os.path.isfile(FNAMEO):
        os.remove(FNAMEO)

    if os.path.isfile(FNAMEA):
        os.remove(FNAMEA)
    
    edgelistAs = []     #selected
    edgelistAsc = []     #selected color
    edgelistAsw = []     #selected color


    edgelistO = []

    edge_colors= ["#737373","#000000","#de3737","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    for i in range(Input.n-1):
        for j in range(i+1, Input.n):

            if Output.X[i][j] > 0.5:
                edgelistAs.append((i,j))
                edgelistAsc.append(edge_colors[2])
                edgelistAsw.append(0.5)

                
            elif Input.A[i,j] > 0.5:
                
                edgelistAs.append((i,j))
                edgelistAsc.append(edge_colors[1])
                edgelistAsw.append(1)

            if Input.A[i,j] > 0.5:
                edgelistO.append((i,j))


    NodeE = set()
    for i in range(Input.n-1):
        for j in range(i+1, Input.n):
            if Output.X[i][j] > 0.5:
                NodeE.update(set([i]))
                NodeE.update(set([j]))


    Positions = {}
    n = Input.n
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])

    node_colors= ["#232ab8","#de3737","#80d189","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [30,50,7000,9000,11000,13000,15000]
    node_shapes = ['s', 'o']

    G = nx.Graph()
    G.add_nodes_from(Positions.keys())
    for a,p in Positions.items():
        G.nodes[a]['pos'] = p 
        if a == Input.sr:
            G.nodes[a]['color'] = node_colors[1]
            G.nodes[a]['edgecolor'] = node_colors[1]
            G.nodes[a]['size'] = node_sizes[1]
            G.nodes[a]['shape'] = node_shapes[0]
        elif a in NodeE:
            G.nodes[a]['color'] = node_colors[0]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['edgecolor'] = node_colors[1]
            G.nodes[a]['shape'] = node_shapes[1]
        else:
            G.nodes[a]['color'] = node_colors[2]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['edgecolor'] = node_colors[2]
            G.nodes[a]['shape'] = node_shapes[1]

    #nx.draw(G, Positions)
    G.add_edges_from(edgelistAs)
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistAsc, width= edgelistAsw)

    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(G,Positions,
                            nodelist = node_list,
                            node_size = [G.nodes[node]['size'] for node in node_list],
                            node_color= [G.nodes[node]['color'] for node in node_list],
                            edgecolors= [G.nodes[node]['edgecolor'] for node in node_list],
                            node_shape = shape)

    plt.savefig(FNAMEA, dpi=300)
    plt.clf()

    G = nx.Graph()
    G.add_nodes_from(Positions.keys())
    for a,p in Positions.items():
        G.nodes[a]['pos'] = p 
        if a == Input.sr:
            G.nodes[a]['color'] = node_colors[1]
            G.nodes[a]['size'] = node_sizes[1]
            G.nodes[a]['shape'] = node_shapes[0]
        else:
            G.nodes[a]['color'] = node_colors[0]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['shape'] = node_shapes[1]

    G.add_edges_from(edgelistO)
    nx.draw_networkx_edges(G,Positions)
    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(G,Positions,
                            nodelist = node_list,
                            node_size = [G.nodes[node]['size'] for node in node_list],
                            node_color= [G.nodes[node]['color'] for node in node_list],
                            node_shape = shape)

    plt.savefig(FNAMEO, dpi=300)
    plt.clf()

    #G = nx.DiGraph()
    #G.add_edges_from(edgelist)
    #nx.draw_networkx(G, arrows=True, **options)
    #pos = nx.spring_layout(G, k=0.15, iterations=2)
    #nx.draw(G, pos)
    #pylab.show() 




