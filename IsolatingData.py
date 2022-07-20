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

def Write_Draw(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_I.png'
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
    

    node_colors= ["#232ab8","#de3737","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
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
        elif a in NodeE:
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

    New_A = np.delete(Input.A,)


    out = open(FNAMED,'wb')
    tmp_dic = {'A':Input.A, 'X':Input.X , 'T':Input.Theta, 'R': Input.sr, 'L':Input.Lmt, 'P':Input.Pos}

    pickle.dump(tmp_dic, out)
    out.close()


def ExtactingNodes():
    
    St = 254
    Ed = 255

    for x in range(St, Ed):

        InputDt = read_data(x)
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
