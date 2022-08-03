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



def Draw_Picture(Input: InputStructure, Output: OutputStructure, WithOld: Boolean = False, YUE: bool = False):

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

    TmpGap = 0
    TmpN   = 0

    if WithOld == True:
        TmpGap = Input.CntAK
        TmpN   = len(Input.OA[0,:])


    edge_colors= ["#737373","#000000","#de3737","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    for i in range(Input.n):
        for j in range(Input.n):

            if Output.X[i][j] > 0.5:
                edgelistAs.append((i,j))
                edgelistAsc.append(edge_colors[2])
                edgelistAsw.append(0.1)

                
            elif Input.A[i][j] > 0.5:
                
                edgelistAs.append((i,j))
                edgelistAsc.append(edge_colors[1])
                edgelistAsw.append(0.2)

            if Input.A[i][j] > 0.5:
                edgelistO.append((i,j))

    
    if WithOld == True:
        for i in range(TmpN-1):
            for j in range(i+1, TmpN):
                if Input.OA[i][j] > 0.5:
                    edgelistAs.append((i+TmpGap,j+TmpGap))
                    edgelistAsc.append(edge_colors[0])
                    edgelistAsw.append(1)

    NodeES = set()
    NodeEN = set()
    for i in range(Input.n):
        for j in range(Input.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            if Input.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))


    NodeEN = NodeEN - NodeES

    Tmp1 = len(NodeES)
    Tmp2 = len(NodeEN)

    Positions = {}
    n = Input.n
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])
    
    if WithOld == True:
        for x in range(TmpN):
            Positions[x+TmpGap] = (Input.OP[x][0],Input.OP[x][1])

    node_colors= ["#232ab8","#f70000","#b1b3b1","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.5,1,7000,9000,11000,13000,15000]
    node_shapes = ['s', 'o']
    
    if WithOld == True:
        OldNodes = [x+TmpGap  for x in Input.LN]
        Tmp3 = len(OldNodes)

    G = nx.Graph()
    G.add_nodes_from(Positions.keys())
    
    ListNodes = [[] for _ in range(5)]

    for a,p in Positions.items():
        G.nodes[a]['pos'] = p 
        if a == Input.sr:
            G.nodes[a]['color'] = node_colors[1]
            G.nodes[a]['edgecolor'] = node_colors[1]
            G.nodes[a]['size'] = node_sizes[1]
            G.nodes[a]['shape'] = node_shapes[0]
            ListNodes[0].append(a)

        elif a in NodeES:
            G.nodes[a]['color'] = node_colors[0]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['edgecolor'] = node_colors[1]
            G.nodes[a]['shape'] = node_shapes[1]
            ListNodes[1].append(a)
        elif a in NodeEN:
            G.nodes[a]['color'] = node_colors[0]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['edgecolor'] = node_colors[0]
            G.nodes[a]['shape'] = node_shapes[1]
            ListNodes[2].append(a)
        elif a in OldNodes:
            G.nodes[a]['color'] = node_colors[2]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['edgecolor'] = node_colors[2]
            G.nodes[a]['shape'] = node_shapes[1]
            ListNodes[3].append(a)
        else:
            G.nodes[a]['color'] = node_colors[2]
            G.nodes[a]['size'] = 0
            G.nodes[a]['edgecolor'] = node_colors[2]
            G.nodes[a]['shape'] = node_shapes[1]
            ListNodes[4].append(a)


    G.add_edges_from(edgelistAs)
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistAsc, width = edgelistAsw)

    for  shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(
                            G,
                            Positions,
                            nodelist = node_list,
                            node_size = [G.nodes[node]['size'] for node in node_list],
                            node_color= [G.nodes[node]['color'] for node in node_list],
                            edgecolors= [G.nodes[node]['edgecolor'] for node in node_list], 
                            node_shape= shape)

    
    plt.savefig(FNAMEA, dpi=1100)
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

    plt.savefig(FNAMEO, dpi=1100)
    plt.clf()


from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result
from draw_graphs import Draw_Picture


if __name__ == '__main__':
    St = 70254
    Ed = 70255
    for x in range(St, Ed):
        InputDt = read_data(x, INCLUDE_OLD = True)

        InputDt.Lmt = int(InputDt.Lmt * 0.5)
        InputDt.Lmt = 20*2
        #InputDt.show()
        ResultDt = Gurobi_Solve(InputDt,Lazy=False)
        print(ResultDt.Time)
        print("Problem solved")
        #Save data and result
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt, WithOld=True)