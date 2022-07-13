
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
import math
import random

import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt



random.seed(0)  # To ensure reproducibility
numberPoints = 40

Lw = 0
Hw = 800
    
Lh = 0
Hh = 600

adjusting_space = 0.9
Limit_space = (float(Hw-Lw) * float(Hh-Lh)* adjusting_space)/numberPoints
Limit_distance = math.sqrt((Limit_space/3.14))
    
MidW = (Lw + Hw)/2
MidH = (Lh + Hh)/2


itr = 0
itr_s = 0
itr_limit = 50000

dist = -0.0
find = False
points = {}

def distance(A , B):

    x = (A[0]-B[0])**2
    y = (A[1]-B[1])**2
    z = x + y
    return math.sqrt(z)


while(itr < numberPoints and itr_s< itr_limit):

    tmp = [random.uniform(Lw, Hw), random.uniform(Lh, Hh)]
    find = False
    for key, value in points.items():
        
        dist = distance(tmp, value)
        if (dist < Limit_distance):
            find = True
            break
    
    if (not find):
        points.update({itr:tmp})
        itr = itr +1 
    
    itr_s = itr_s + 1


if (itr_s == itr_limit):

    print("cannot creat the instance!!")
    exit(2)




from scipy.spatial import Delaunay
tri = Delaunay(list(points.values()))

#print(tri.simplices)

# finding the center 
min_k = -1
min_v = 999999999.0

for key, value in points.items():
        
    dist = distance([MidW, MidH], value)
    if (dist < min_v):
        min_v = dist
        min_k = key


# extracting the edges
edge_list = []
for tri in tri.simplices:
    edge_list.append([tri[0], tri[1]])
    edge_list.append([tri[1], tri[2]])
    edge_list.append([tri[2], tri[0]])


node_colors= ["#232ab8","#de3737","#80d189","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
node_sizes = [30,50,7000,9000,11000,13000,15000]
node_shapes = ['s', 'o']


G = nx.Graph()
G.add_nodes_from(points.keys())
for a,p in points.items():
    G.nodes[a]['pos'] = p 
    if a == min_k:
        G.nodes[a]['color'] = node_colors[1]
        G.nodes[a]['size'] = node_sizes[1]
        G.nodes[a]['shape'] = node_shapes[0]
        G.nodes[a]['label'] = str(a)
    else:
        G.nodes[a]['color'] = node_colors[0]
        G.nodes[a]['size'] = node_sizes[0]
        G.nodes[a]['shape'] = node_shapes[1]
        G.nodes[a]['label'] = str(a)


G.add_edges_from(edge_list)

#nx.draw(G, Positions)
nx.draw_networkx_edges(G,points)

for shape in set(node_shapes):
    # the nodes with the desired shapes
    node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
    nx.draw_networkx_nodes(G,points,
                        nodelist = node_list,
                        node_size = [G.nodes[node]['size'] for node in node_list],
                        node_color= [G.nodes[node]['color'] for node in node_list],
                        node_shape = shape, 
                        label = [G.nodes[node]['label'] for node in node_list]
                        )

    nx.draw_networkx_labels(G,points, font_size=6)

CurrectFolder = os.path.dirname(os.path.abspath(__file__))
GNNPICOUT = CurrectFolder + "/GNNPICOUT"
if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

FNAMEO = GNNPICOUT + '/Tinstance' + '_O.png'
plt.savefig("Tinstance", dpi=300)
plt.clf()

exit(12)

import matplotlib.pyplot as plt

Xs = [x[0] for x in list(points.values())]
Ys = [x[1] for x in list(points.values())]

print(list(points.values()))


plt.triplot(Xs, Ys, tri.simplices)
plt.plot(Xs, Ys, 'o')
plt.show()
exit(12)



x, y = np.random.rand(2, 30)
g = ig.Graph(30)
g.vs['x'] = x
g.vs['y'] = y

# Calculate the delaunay triangulation, and add the edges into the original graph
coords = g.layout_auto().coords
delaunay = Delaunay(coords)


# Plot the graph
fig, ax = plt.subplots()
ig.plot(
    g,
    target=ax,
    vertex_size=0.04,
    vertex_color="lightblue",
    edge_width=0.8
)
plt.show()
