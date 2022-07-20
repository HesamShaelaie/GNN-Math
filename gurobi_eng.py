import os
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from data import CreateData
from data_structures import InputStructure
from data_structures import OutputStructure
import time
from arg_parse import wait_key

def Gurobi_Solve(InputData: InputStructure, Lazy = True):

    try:
        #Data input
        N = InputData.n
        Srow = InputData.sr
        Lmt = InputData.Lmt

        #Data result
        OutData = OutputStructure()

        # Create a new model
        m = gp.Model("quadratic")
    
        # Variables        
        x = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="x")
        
        # Set objective
        obj = gp.QuadExpr()
        
        # Set quadratic part
        cnt_negetive_trm = 0
        for Pindex in range(N):
            z = IndexMaker(N, Srow, Pindex)

            for i1,j1,i2,j2 in z:
                obj.add(InputData.XTW[Pindex]*x[i1,j1]*x[i2,j2])

            if InputData.XTW[Pindex] <= 0:
                cnt_negetive_trm = cnt_negetive_trm + 1
                print("We have negative/zero coefficient in objective function!!")
                exit(3355)

        # Geting the number of quadratic term in objective function
        OutData.NQ =obj.size()

        m.setObjective(obj , GRB.MAXIMIZE)
        m.params.NonConvex = 2

        # Adding constraints

        # Constraint (1)
        for i in range(N):
            for j in range(N):
                m.addConstr(x[i,j] <= InputData.A[i,j])


        #constraint (2)
        for i in range(N-1):
            for j in range(i+1, N):
                m.addConstr(x[i,j] == x[j,i])

        
        #constraint (3)
        m.addConstr(gp.quicksum(x[i,j] for i in range(N) for j in range(N)) <= Lmt)

        # lazy optimization parameters
        m.Params.LazyConstraints = 1
        m._var = x

        # running the algorithm
        begin = time.time()
        if Lazy == True:
            m.optimize(subtourelim)
        else:
            m.optimize()
        end = time.time()

        OutData.Time = end-begin
        OutData.X = x.X
        OutData.Obj = m.objVal
        
        # testing the solution
        test_x = x.X
        Visited = subtour(test_x, InputData.n)
        for x in Visited:
            if not x:
                print("Solution is not valid!!")
        print(OutData.Time)
        return OutData
        
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    except AttributeError:
        #printf("%s\n", GRBgeterrormsg(env))
        print('Encountered an attribute error')


def IndexMaker(Size, x, y):
    return [(x,i,i,y) for i in range(Size)] 


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._var)
        # find the shortest cycle in the selected edge list
        
        n = len(vals[0,:])
        
        SubGraph = subtour(vals, n)
        
        Cnt = 0
        for x in SubGraph:
            if x == True:
                Cnt = Cnt + 1

        if Cnt == 0:
            return

        if Cnt < n:
            # add subtour elimination constr. for every pair of cities in tour
            YesVisited = [x for x in range(n) if SubGraph[x] == True]
            NoVisited = [x for x in range(n) if SubGraph[x] == False]
            tmp = gp.LinExpr()

            for x in YesVisited:
                for y in NoVisited:
                    tmp.add(model._var[x, y])
            
            model.cbLazy(tmp >= 1)


# Given a tuplelist of edges, find the shortest subtour

def DFS_Nonrecursive(vals, n, v, visited):

    # Mark current node as visited
    Clist = np.zeros(n, dtype=np.int16)
    Clist[0] = v
    cnt = 1

    while cnt > 0:
        v = Clist[cnt-1]
        cnt = cnt - 1 
    # do for every edge (v, u)
        for u in range(n):
            if vals[v,u] > 0.5:
                if not visited[u]:
                    Clist[cnt] = u
                    cnt = cnt + 1
                    visited[u] = True


def DFS(vals, n, v, visited):
    # mark current node as visited
    visited[v] = True
    
    # do for every edge (v, u)
    for u in range(n):
        if vals[v,u] > 0.5:
            if not visited[u]:
                DFS(vals, n, u, visited)


def subtour(vals, n):
    
    i = -1
    j = -1
    for x in range(n):
        for y in range(n):
            if vals[x,y]> 0.5:
                i = x
                break
        if i != -1:
            break

    visited = [False] * n
    if i == -1:
        return visited

    DFS_Nonrecursive(vals, n, i, visited)

    return visited

