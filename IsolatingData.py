from tkinter import Y
from turtle import color
from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
import pylab
import os
import pickle
import ssl

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from mpl_toolkits.basemap import Basemap as Basemap

import os
from data_structures import OutputStructure


def Draw_Graph_O(Input: InputStructure):

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

    for i in range(Input.n):
        for j in range(Input.n):
            if Input.CopyA[i][j] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])

    '''
    #drawing on the map
    plt.figure(figsize = (12,8))
    m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
    urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
    mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
    pos = {}
    for count, elem in enumerate(pos_data['nodes']):
        pos[elem] = (mx[count], my[count])
    nx.draw_networkx_edges(G, pos = pos, edge_color='blue', alpha=0.1, arrows = False)
    m.drawcountries(linewidth = 2)
    m.drawstates(linewidth = 0.2)
    m.drawcoastlines(linewidth=2)
    plt.tight_layout()
    plt.savefig("map.png", dpi = 300)
    plt.show()
    '''

    Positions = {}
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])
    

    node_colors= ["#232ab8","#de3737","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,7000,9000,11000,13000,15000]
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

    options = {
    'arrows': True,
    #'node_color': 'blue',
    #'node_size': 100,
    #'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 0.1,
    }

    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width=0.1)#, **options)

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

    plt.savefig(FNAMEI, dpi=1100)
    plt.clf()


def Draw_Graph_K(Input: InputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_K.png'       # Whole nodesh and arcs

    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)

    edgelistO = [] # original
    edgelistC = [] # color of original
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    for i in range(Input.n):
        for j in range(Input.n):
            if Input.AA[i][j] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])

    '''
    #drawing on the map
    plt.figure(figsize = (12,8))
    m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
    urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
    mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
    pos = {}
    for count, elem in enumerate(pos_data['nodes']):
        pos[elem] = (mx[count], my[count])
    nx.draw_networkx_edges(G, pos = pos, edge_color='blue', alpha=0.1, arrows = False)
    m.drawcountries(linewidth = 2)
    m.drawstates(linewidth = 0.2)
    m.drawcoastlines(linewidth=2)
    plt.tight_layout()
    plt.savefig("map.png", dpi = 300)
    plt.show()
    '''

    Positions = {}
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])
    

    node_colors= ["#232ab8","#de3737","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,7000,9000,11000,13000,15000]
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

    options = {
    'arrows': True,
    #'node_color': 'blue',
    #'node_size': 100,
    #'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 0.1,
    }

    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width=0.1)#, **options)

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

    plt.savefig(FNAMEI, dpi=1100)
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
    edgelistW = []
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]


    for i in range(Input.n-1):
        for j in range(i+1,Input.n):
            if Output.X[i][j] > 0.5 or Output.X[j][i] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])
                edgelistW.append(0.3)
            elif Input.A[i][j] > 0.5 or Input.A[j][i] > 0.5: 
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[0])
                edgelistW.append(0.05)
   

    NodeES = set()
    NodeEN = set()

    for i in range(Input.n):
        for j in range(Input.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            elif Input.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))
    
    NodeEN = NodeEN - NodeES

    Positions = {}
    
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])

    node_colors= ["#232ab8","#c26b29","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,7000,9000,11000,13000,15000]
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
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width = edgelistW)
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

    plt.savefig(FNAMEI, dpi=1000)
    plt.clf()
    
    exit(3)
    # ===================================================
    # ========   creating new set of data  ==============
    # ===================================================
    
    NodeNotInList = [x for x in range(Input.n) if x not in NodeES]

    # GETTING ALL THE NODES for the edge which are not on the map
    
    ReEdge = np.copy(Input.A)
    for i in range(Input.n):
        for j in range(Input.n):
            if Output.X[i][j] > 0.5:
                ReEdge[i][j] = 0
                

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

    New_OrgA = np.copy(Input.OriginalA)

    New_OrgA = np.delete(New_OrgA,NodeNotInList, 0)
    New_OrgA = np.delete(New_OrgA,NodeNotInList, 1)

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
    tmp_dic = {'A':New_A, 'X':New_X , 'T':Input.Theta, 'R': New_sr, 'L':New_Lmt, 'P':NewPositions, 'OA':ReEdge, 'OP':Input.Pos, 'LN': list(NodeEN), 'ORGA': New_OrgA}

    pickle.dump(tmp_dic, out)
    out.close()

#pems-bay-K=5-directed-A 900004
#metr-la-K=5-directed-A 900005


def DrawOnMap(Input: InputStructure, Output: OutputStructure, WithKTwo: bool = False):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_M.png'
    


    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)

    edgelistO = []
    edgelistC = []
    edgelistW = []
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]


    for i in range(Input.n-1):
        for j in range(i+1,Input.n):
            if Output.X[i][j] > 0.5 or Output.X[j][i] > 0.5:
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])
                edgelistW.append(0.3)
            elif Input.A[i][j] > 0.5 or Input.A[j][i] > 0.5: 
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[0])
                edgelistW.append(0.05)
   

    NodeES = set()
    NodeEN = set()

    for i in range(Input.n):
        for j in range(Input.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            elif Input.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))
    
    NodeEN = NodeEN - NodeES

    MinLat = Input.Pos[0][0]
    MinLon = Input.Pos[0][1]

    MaxLat = Input.Pos[0][0]
    MaxLon = Input.Pos[0][1]

    for x in range(Input.n):
        if MinLat > Input.Pos[x][0]:
            MinLat = Input.Pos[x][0]

        if MaxLat < Input.Pos[x][0]:
            MaxLat = Input.Pos[x][0]

        if MinLon > Input.Pos[x][1]:
            MinLon = Input.Pos[x][1]

        if MaxLon < Input.Pos[x][1]:
            MaxLon = Input.Pos[x][1]
        

    m = Basemap(
        projection='merc',
        llcrnrlon=MinLon,
        llcrnrlat=MinLat,
        urcrnrlon=MaxLon,
        urcrnrlat=MaxLat,
        lat_ts=0,
        epsg = 3309,
        resolution='i',
        suppress_ticks=True)

    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 12000, verbose= True)
    Positions = {}


    lats = [Input.Pos[x][0] for x in range(Input.n)]
    lons = [Input.Pos[x][1] for x in range(Input.n)]
    
    mx,my=m(lons,lats)

    for x in range(Input.n):
        Positions[x]=(mx[x],my[x])

    node_colors= ["#232ab8","#c26b29","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,7000,9000,11000,13000,15000]
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
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width = edgelistW)
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

    # Now draw the map
    m.drawcountries()
    m.drawstates()
    m.bluemarble()
    plt.savefig(FNAMEI, dpi=1000)
    plt.clf()
    


def ExtactingNodes_YUE():
    
    
    St = 900004
    Ed = 900005

    for x in range(St, Ed):

        InputDt = read_data(x, INCLUDE_OLD=False, YUE=True)
        

        InputDt.blank_X()
        InputDt.blank_T()

        #Somecheckings(InputDt)
        
        InputDt.recalculate(K=5, Rho=3, ResetLimit=True, WithAdjustment=True)

        #SecondaryCheck(InputDt)
        #FindMaxNeighbours(InputDt)
        
        InputDt.sr = 5
        #InputDt.recalculate(K=2, ResetLimit=True, WithAdjustment=True)

        DrawBasedOnA(InputDt)
        #SecondaryCheck(InputDt)
        #FindMaxNeighbours(InputDt)

        #Somecheckings(InputDt)
        
        Draw_Graph_O(InputDt)
        Draw_Graph_K(InputDt)
        InputDt.Lmt = 654

        #ResultDt = Gurobi_Solve(InputDt, Lazy= False, YUE= False, UndirectionalConstraint=True, Testing= True)
        ResultDt = Gurobi_Solve(InputDt, Lazy= False, UndirectionalConstraint=False)

        Write_X_Only_Nodes(InputDt, ResultDt)

        InputDt.reset_X()
        InputDt.reset_T()
        #Save data and result
        print("CntX= %d"%ResultDt.CntX)
        #DrawOnMap(InputDt, ResultDt, WithKTwo= True)
        Write_Draw(InputDt, ResultDt, WithKTwo= True)


def Somecheckings(InputDt: InputStructure):

    CntB = 0
    for x in range(InputDt.n):
        for y in range(InputDt.n):
            if InputDt.A[x][y]>0.5:
                CntB = CntB + 1
    
    print("the total is %d"%CntB)

    for x in range(InputDt.n):
        for y in range(InputDt.n):
            if InputDt.A[x][y]>0.5:
                if InputDt.A[y][x]<0.5:
                    print("In un directed graph there is a problem!!")
                    exit(33)
    
    for x in range(InputDt.n):
        if InputDt.A[x][x]> 0.5:
            print("diagnal is not zero!!")
            exit(33)

def SecondaryCheck(InputDt: InputStructure):
    k = InputDt.K
    k = k*2

    n = InputDt.n
    A = np.copy(InputDt.A)
    B = A@A

    r = InputDt.sr

    for x in range(n):
        B[x][x] = 0

    cnt = 0 
    for y in range(n):
        if B[r][y]>0.5:
            cnt = cnt + 1
    
    for x in range(n):
        if B[x][r]>0.5:
            cnt = cnt + 1

    print("Hub (%d) have (%d) neighbours at K=%d "%(r, cnt, k))
    


def FindMaxNeighbours(InputDt: InputStructure):

    k = InputDt.K
    k = k*2
    n = InputDt.n
    A = np.copy(InputDt.A)
    B = A@A

    r = InputDt.sr

    Max = -1
    IndxR = -1

    for x in range(n):
        B[x][x] = 0

    for r in range(n):
        cnt = 0 
        for y in range(n):
            if B[r][y]>0.5:
                cnt = cnt + 1
        
        for x in range(n):
            if B[x][r]>0.5:
                cnt = cnt + 1

        if Max < cnt:
            Max = cnt
            IndexR = cnt

    print("Max neightbours belong to Hub (%d) with (%d) neighbours at K=%d "%(IndexR, Max, k))
    
def DrawBasedOnA(Input: InputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_A.png'


    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)


    edgelistO = []
    edgelistC = []
    edgelistW = []
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]

    A = np.copy(Input.A)
    for i in range(Input.n-1):
        for j in range(i+1,Input.n):
            if (i== Input.sr or j==Input.sr) and (A[i][j] > 0.5 or A[j][i] > 0.5):
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[1])
                edgelistW.append(0.3)
            elif Input.A[i][j] > 0.5 or Input.A[j][i] > 0.5: 
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[0])
                edgelistW.append(0.05)
   

    NodeES = set()
    NodeEN = set()

    for i in range(Input.n):
        for j in range(Input.n):
            if (i==Input.sr or j==Input.sr) and A[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            elif Input.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))
    
    NodeEN = NodeEN - NodeES

    Positions = {}
    
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])

    node_colors= ["#232ab8","#c26b29","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,7000,9000,11000,13000,15000]
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
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width = edgelistW)
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

    plt.savefig(FNAMEI, dpi=1000)
    plt.clf()
    

def Write_X_Only_Nodes(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMEI = GNNPICOUT + '/' + Input.Fname + '_N.png' #nodes
    FNAMED = GNNINPUT + '/' + str(int(Input.Fname)+70000) + '.txt'


    if os.path.isfile(FNAMEI):
        os.remove(FNAMEI)

    if os.path.isfile(FNAMED):
        os.remove(FNAMED)

    edgelistO = []
    edgelistC = []
    edgelistW = []
    
    edge_colors= ["#737373","#000000","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]


    for i in range(Input.n-1):
        for j in range(i+1,Input.n):
            if Input.A[i][j] > 0.5 or Input.A[j][i] > 0.5: 
                edgelistO.append((i,j))
                edgelistC.append(edge_colors[0])
                edgelistW.append(0.05)
   

    NodeES = set()
    NodeEN = set()

    for i in range(Input.n):
        for j in range(Input.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            elif Input.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))
    
    NodeEN = NodeEN - NodeES

    Positions = {}
    
    for x in range(Input.n):
        Positions[x]=(Input.Pos[x][0],Input.Pos[x][1])

    node_colors= ["#232ab8","#c26b29","#a9b0aa","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    node_sizes = [0.1,0.2,0.3,9000,11000,13000,15000]
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
            G.nodes[a]['size'] = node_sizes[2]
            G.nodes[a]['shape'] = node_shapes[1]
        else:
            G.nodes[a]['color'] = node_colors[2]
            G.nodes[a]['size'] = node_sizes[0]
            G.nodes[a]['shape'] = node_shapes[1]

    G.add_edges_from(edgelistO)

    #nx.draw(G, Positions)
    nx.draw_networkx_edges(G, Positions, edge_color=edgelistC, width = edgelistW)
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

    plt.savefig(FNAMEI, dpi=1000)
    plt.clf()
    



if __name__ == '__main__':
    #ExtactingNodes()
    ExtactingNodes_YUE()
