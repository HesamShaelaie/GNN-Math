import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from data import CreateData
import os

# You must set the parameter LazyConstraint=1. Otherwise, Gurobi might apply dual presolve reductions that are not valid for the lazy constraints.
# Larger values for this attribute cause the constraint to be pulled into the model more aggressively. 
# With a value of 1, the constraint can be used to cut off a feasible solution, but it won't necessarily be pulled in if another lazy constraint also cuts off the solution.
# With a value of 2, all lazy constraints that are violated by a feasible solution will be pulled into the model.
# With a value of 3, lazy constraints that cut off the relaxation solution at the root node are also pulled in.


np.random.seed(2021)

N = 20 #matrix n by n
D1 = 5      #matrix n by d1
D2 = 6      #matrix d1 by d2
Srow = 3    #selected row
Frac = 0.5 
FSub = 0.5

def IndexMaker(Size, x, y):
    return [(x,i,i,y) for i in range(Size)] 


# Code to Measure time taken by program to execute.
import time

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:                                            #???????
        vals = model.cbGetSolution(model._var)
        # find the shortest cycle in the selected edge list
        n = len(vals[0,:])
        #n = testdata.n
        SubGraph = subtour(vals)
        #
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

def DFS(vals, v, visited):

    # mark current node as visited
    visited[v] = True
    #n = len(visited)
    n = testdata.n
    # do for every edge (v, u)
    for u in range(n):
        if vals[v,u] > 0.5:
            if not visited[u]:
                DFS(vals, u, visited)


def DFSX(vals, v, visited):

    # mark current node as visited
    visited[v] = True
    #n = len(visited)
    n = testdata.n
    # do for every edge (v, u)
    for u in range(n):
        if vals[v,u].X > 0.5:
            if not visited[u]:
                DFSX(vals, u, visited)


def subtour(vals):
    # make a list of edges selected in the solution
    
    #n = len(vals[0,:].X)
    n = testdata.n
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
    DFS(vals, i, visited)

    return visited

def subtourX(vals):
    # make a list of edges selected in the solution
    
    #n = len(vals[0,:].X)
    n = testdata.n
    i = -1
    j = -1
    for x in range(n):
        for y in range(n):
            if vals[x,y].X > 0.5:
                i = x
                break
        if i != -1:
            break

    visited = [False] * n
    DFSX(vals, i, visited)

    return visited

testdata = CreateData(N, D1, D2, Srow, Frac, FSub)
testdata.Generate_Random_v2()
testdata.DoTheMath()
testdata.getInfo()


input("Press Enter to continue...")

try:

    # Create a new model
    m = gp.Model("quadratic")
   
    # Number of Variables
    #x = m.addMVar(shape=(N,N), vtype=GRB.CONTINUOUS, name="x", lb=0.0, ub=1.0)
    x = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="x")
    #y = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="y")
    
    # Why we need the y?? for the next version of the problem throw away the y and from beginning go for the boolean X
    
    
    # Set objective
    obj = gp.QuadExpr()
    
    # Set quadratic part
    for Pindex in range(N):
        z = IndexMaker(N, Srow, Pindex)

        for i1,j1,i2,j2 in z:
            obj.add(testdata.XTW[Pindex]*x[i1,j1]*x[i2,j2])

    #print("", obj.size())
    #exit(11)

    m.setObjective(obj , GRB.MAXIMIZE)
    #m.setObjective(obj , GRB.MINIMIZE)
    m.params.NonConvex = 2

    for i in range(N):
        for j in range(N):
            m.addConstr(x[i,j] <= testdata.A[i,j])

    for i in range(N-1):
        for j in range(i+1, N):
            m.addConstr(x[i,j] == x[j,i])

    Lmt = int(testdata.nedge * FSub)
    
    m.addConstr(gp.quicksum(x[i,j] for i in range(N) for j in range(N)) <= Lmt)

    # store starting time
    begin = time.time()
    #m._vars = x
    m.Params.LazyConstraints = 1
    m._var = x
    m.optimize(subtourelim)

    end = time.time()
    print("===============================")
    print("===============================")
    print("===============================")
    print(x.X)
    print("===============================")
    print("===============================")
    print("===============================")
    print(x.X[1,2])
    print('Obj: %g' % m.objVal)
    print("===============================")
    print("===============================")
    print("===============================")
    print("===============================")
    test_x = m._var
    #test_x = m.cbGetSolution(m._vars)
    #print(test_x[1,3].X)

    Visited = subtourX(test_x)
    print(Visited)
    print(f"Total runtime of the program is {end - begin}")

    #print(test_x)


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")

except AttributeError:
    #printf("%s\n", GRBgeterrormsg(env))
    print('Encountered an attribute error')