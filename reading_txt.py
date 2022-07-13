
from ast import While
from numpy import float64
from ast import For
from ctypes import sizeof
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os
from data_structures import InputStructure
from data_structures import OutputStructure

positions = {}
edgelistA = []
with open('/Users/hesamshaelaie/Documents/Research/Delaunay-triangulation/Delaunay-triangulation/TInstance.txt') as f:
    nn = int(next(f))
    ne = int(next(f))
    print(nn)
    print(ne)

    rw = 0
    while rw < nn:
        tmp = next(f).split()
        if tmp:
            positions.update({int(tmp[0]): (float64(tmp[1]),float64(tmp[2]))})
            print(tmp)
            rw = rw + 1

    while rw < ne:
        tmp = next(f).split()
        if tmp:
            edgelistA.append((int(tmp[0]),int(tmp[1])))
            rw = rw + 1
    
    LenList = len(edgelistA)
    LenSet = len(set(edgelistA))

    if LenList != LenSet:
        print("LenList != LenSet")
        exit(12)
    

node_colors= ["#232ab8","#de3737","#80d189","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
node_sizes = [30,50,7000,9000,11000,13000,15000]
node_shapes = ['s', 'o']


G = nx.Graph()
G.add_nodes_from(positions.keys())
for a,p in positions.items():
    G.nodes[a]['pos'] = p 
    if a == 10:
        G.nodes[a]['color'] = node_colors[1]
        G.nodes[a]['size'] = node_sizes[1]
        G.nodes[a]['shape'] = node_shapes[0]
        G.nodes[a]['label'] = str(a)
    else:
        G.nodes[a]['color'] = node_colors[0]
        G.nodes[a]['size'] = node_sizes[0]
        G.nodes[a]['shape'] = node_shapes[1]
        G.nodes[a]['label'] = str(a)


G.add_edges_from(edgelistA)

#nx.draw(G, Positions)
nx.draw_networkx_edges(G,positions)

for shape in set(node_shapes):
    # the nodes with the desired shapes
    node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
    nx.draw_networkx_nodes(G,positions,
                        nodelist = node_list,
                        node_size = [G.nodes[node]['size'] for node in node_list],
                        node_color= [G.nodes[node]['color'] for node in node_list],
                        node_shape = shape, 
                        label = [G.nodes[node]['label'] for node in node_list]
                        )

    nx.draw_networkx_labels(G,positions, font_size=6)

CurrectFolder = os.path.dirname(os.path.abspath(__file__))
GNNPICOUT = CurrectFolder + "/GNNPICOUT"
if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

FNAMEO = GNNPICOUT + '/Tinstance' + '_O.png'
plt.savefig("Tinstance", dpi=300)
plt.clf()
