import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from data import CreateData


np.random.seed(2021)
N = 10
d1 = 5
d2 = 6
Srow = 5  #candidate row for the calculation
Lmt = 0

try:

    # Create a new model
    m = gp.Model("quadratic")
    

    # Number of Variables
    x = m.addMVar(shape=(N,N), vtype=GRB.CONTINUOUS, name="x", lb=0.0, ub=1.0)
    y = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="y")
    

    # Set objective
    obj = gp.QuadExpr()
    
    # Set quadratic part
    for i in range(N):
        for j in range(N):
            for k in range(N):
                obj.add(C[i,j]*x[i,k]*x[k, j])
    
    
    #m.setObjective(obj , GRB.MINIMIZE)
    m.setObjective(obj , GRB.MAXIMIZE)

    for i in range(N):
        for j in range(N):
            m.addConstr(x[i,j] <= A[i,j]*y[i,j])

    m.addConstr(gp.quicksum(y[i,j] for i in range(N) for j in range(N)) <= Lmt )
    

    m.optimize()

    print(x.X)
    print('Obj: %g' % m.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')