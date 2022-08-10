from tkinter import Y
from turtle import color
from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from gurobi_eng import Gurobi_SecondObj
import pylab
import os
import pickle
import ssl
from write_output import Write_Result
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from mpl_toolkits.basemap import Basemap as Basemap

from draw_graphs import Draw_Graph_K
from draw_graphs import Draw_Graph_O
from draw_graphs import DrawOnMap
from draw_graphs import DrawBasedOnA
from draw_graphs import Write_X_Only_Nodes
from draw_graphs import Write_X_Endg_Nodes
from extract_NodeEdges import Write_Node_Edges
from extract_NodeEdges import Write_Node_Edges_Only

import os
from data_structures import OutputStructure


def Sepreate_Data(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT"
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)

    FNAMED = GNNINPUT + '/' + str(int(Input.Fname)+70000) + '.txt'

    if os.path.isfile(FNAMED):
        os.remove(FNAMED)

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

def ExtactingNodes_YUE():
    
    BlackOut = False
    St = 900006
    Ed = 900007

    for x in range(St, Ed):

        InputDt = read_data(x, INCLUDE_OLD=False, YUE=True, INCLUDE_ID=True)
        

        if BlackOut:
            InputDt.blank_X()
            InputDt.blank_T()

        #Somecheckings(InputDt)
        InputDt.A = np.transpose(np.copy(InputDt.CopyA))
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
        InputDt.Lmt = 5

        #ResultDt = Gurobi_Solve(InputDt, Lazy= False, YUE= False, UndirectionalConstraint=True, Testing= True)
        #ResultDt = Gurobi_Solve(InputDt, Lazy= False, UndirectionalConstraint=False)
        ResultDt = Gurobi_SecondObj(InputDt, Lazy= False, UndirectionalConstraint=False)
        
        Write_X_Only_Nodes(InputDt, ResultDt)

        if BlackOut:
            InputDt.reset_X()
            InputDt.reset_T()
        #Save data and result

        print("CntX= %d"%ResultDt.CntX)
        #DrawOnMap(InputDt, ResultDt, WithKTwo= True)
        
        Write_X_Endg_Nodes(InputDt, ResultDt)
        #Sepreate_Data(InputDt, ResultDt)

        Write_Result(InputDt, ResultDt)

        Write_Node_Edges(InputDt, ResultDt)
        Write_Node_Edges_Only(InputDt, ResultDt)


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
    

if __name__ == '__main__':
    #ExtactingNodes()
    ExtactingNodes_YUE()
