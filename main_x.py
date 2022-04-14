import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from data import CreateData


np.random.seed(2021)

N = 10 #matrix n by n
D1 = 5      #matrix n by d1
D2 = 6      #matrix d1 by d2
Srow = 3    #selected row
Frac = 0.9 
FSub = 0.2

def IndexMaker(Size, x, y):
    return [(x,i,i,y) for i in range(Size)]


try:

    # Create a new model
    m = gp.Model("quadratic")
    testdata = CreateData(N, D1, D2, Srow, Frac)
    testdata.Generate_Random_v2()
    testdata.DoTheMath()

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

    #m._vars = x
    #m.Params.LazyConstraints = 1
    
    m.optimize()

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
    #test_x = m._vars()
    #test_x = m.cbGetSolution(m._vars)
    #print(test_x)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")

except AttributeError:
    #printf("%s\n", GRBgeterrormsg(env))
    print('Encountered an attribute error')