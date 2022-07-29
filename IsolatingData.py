from turtle import color
from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
import pylab
import os
import pickle

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import os
from data_structures import OutputStructure
import os

def Draw_original(Input: InputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_O.png'       # Whole nodesh and arcs

    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)

    edgelistO = [] # original
    edgelistC = [] # color of original
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    for i in range(Input.n-1):
        for j in range(i+1, Input.n):
            if Input.A[i,j] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])



    Positions = {}
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])
    

    node_colors= ["#232ab8","#de3737","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [2,5,7000,9000,11000,13000,15000]
    node_shapes = ['s', 'o']


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
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width=0.4)
    '''
    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(G,Positions,
                            nodelist = node_list,
                            node_size = [G.nodes[node]['size'] for node in node_list],
                            node_color= [G.nodes[node]['color'] for node in node_list],
                            node_shape = shape)
    '''

    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(
                                G,
                                Positions,
                                nodelist = node_list,
                                node_size  = [G.nodes[node]['size'] for node in node_list],
                                node_color = [G.nodes[node]['color'] for node in node_list],
                                node_shape = shape
                            )

    plt.savefig(FNAMEI, dpi=300)
    plt.clf()
    

def Write_Draw(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_X.png'
    FNAMED = GNNINPUT + '/' + str(int(Input.Fname)+70000) + '.txt'


    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)

    if os.path.isfile(FNAMED):
        os.remove(FNAMED)
    
    edgelistO = []
    edgelistC = []
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    for i in range(Input.n-1):
        for j in range(i+1, Input.n):
            if Output.X[i][j] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])
            elif Input.A[i,j] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[0])


    NodeES = set()
    NodeEN = set()
    for i in range(Input.n-1):
        for j in range(i+1, Input.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            elif Input.A[i,j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))
    
    NodeEN = NodeEN - NodeES


    Positions = {}
    n = Input.n
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])
    

    node_colors= ["#232ab8","#c26b29","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [30,50,7000,9000,11000,13000,15000]
    node_shapes = ['s', 'o']


    G = nx.Graph()
    G.add_nodes_from(Positions.keys())
    for a,p in Positions.items():
        G.nodes[a]['pos'] = p 
        if a == Input.sr:
            G.nodes[a]['color'] = node_colors[1]
            G.nodes[a]['size'] = node_sizes[1]
            G.nodes[a]['shape'] = node_shapes[0]
        elif a in NodeES:
            G.nodes[a]['color'] = node_colors[0]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['shape'] = node_shapes[1]
        else:
            G.nodes[a]['color'] = node_colors[2]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['shape'] = node_shapes[1]

    G.add_edges_from(edgelistO)

    #nx.draw(G, Positions)
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC)
    '''
    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(G,Positions,
                            nodelist = node_list,
                            node_size = [G.nodes[node]['size'] for node in node_list],
                            node_color= [G.nodes[node]['color'] for node in node_list],
                            node_shape = shape)
    '''

    for shape in set(node_shapes):
        # the nodes with the desired shapes
        node_list = [node for node in G.nodes() if G.nodes[node]['shape'] == shape]
        nx.draw_networkx_nodes(
                                G,
                                Positions,
                                nodelist = node_list,
                                node_size  = [G.nodes[node]['size'] for node in node_list],
                                node_color = [G.nodes[node]['color'] for node in node_list],
                                node_shape = shape
                            )

    plt.savefig(FNAMEI, dpi=300)
    plt.clf()

    # ===================================================
    # ========   creating new set of data  ==============
    # ===================================================


    
    NodeNotInList = [x for x in range(Input.n) if x not in NodeES]

    # GETTING ALL THE NODES for the edge which are not on the map
    
    ReEdge = np.copy(Input.A)
    for i in range(Input.n-1):
        for j in range(i+1, Input.n):
            if Output.X[i][j] > 0.5:
                ReEdge[i,j] = 0
                ReEdge[j,i] = 0

    # Color edge
    ALLNode = [x for x in range(Input.n)]

    for t in NodeNotInList:
        for y in range(Input.n):
            if t == y:
                ALLNode[y] = -1
            elif t < y:
                ALLNode[y] = ALLNode[y]-1

    NewPositions = {}
    for x in range(Input.n):
        if ALLNode[x] != -1:
            NewPositions.update({ALLNode[x]:Input.Pos[x]})


    New_A = np.copy(Input.A)
    for x in range(Input.n):
        for y in range(Input.n):
            if Output.X[x][y]>0.5:
                New_A[x,y] = 1
            else:
                New_A[x,y] = 0

    New_A = np.delete(New_A,NodeNotInList, 0)
    New_A = np.delete(New_A,NodeNotInList, 1)

    New_X = np.delete(Input.X,NodeNotInList, 0)
    New_n = Input.n - len(NodeNotInList)
    New_Lmt = 0

    for x in range(New_n):
        for y in range(New_n):
            if New_A[x,y]>0.5:
                New_Lmt = New_Lmt + 1


    New_sr = ALLNode[Input.sr]
    if New_sr == -1:
        print("New_sr == -1")
        exit(993)

    out = open(FNAMED,'wb')
    tmp_dic = {'A':New_A, 'X':New_X , 'T':Input.Theta, 'R': New_sr, 'L':New_Lmt, 'P':NewPositions, 'OA':ReEdge, 'OP':Input.Pos, 'LN': list(NodeEN)}

    pickle.dump(tmp_dic, out)
    out.close()


def ExtactingNodes():
    
    St = 254
    Ed = 256

    for x in range(St, Ed):

        InputDt = read_data(x, INCLUDE_OLD=False, YUE=False)

        Draw_original(InputDt)

        
        cnt = 0
        for x in range(InputDt.n):
            for y in range(InputDt.n):
                if InputDt.A[x,y]>0.5:
                    cnt = cnt + 1

        InputDt.Lmt = cnt + 100

        ResultDt = Gurobi_Solve(InputDt, Lazy= False)
        
        #Save data and result
        Write_Draw(InputDt, ResultDt)

if __name__ == '__main__':
    ExtactingNodes()
