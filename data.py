from ctypes import sizeof
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os
import pickle
import sys



from datetime import datetime


now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
print("date and time =", dt_string)	

LIMIT_ITR = 10000

class CreateData:

    def __init__(self, N, D1, D2, Srow, Fraction, FSub=-1):
        self.n = N
        self.d1 = D1
        self.d2 = D2
        self.sr = Srow
        self.fr = Fraction
        self.AXT = np.empty
        self.AXTR = np.empty
        self.nedge = N**2
        self.FSub = FSub
    def show_par(self):
        print(self.n)
        print(self.d1)
        print(self.d2)
        print(self.sr)
    
    def Generate_Random_v1(self):

        self.A = np.random.randint(0,2, size=(self.n, self.n))
        UpCnt = 0

        for i in range(self.n - 1):
            for j in range(i + 1 ,self.n):
                self.A[j][i] = self.A[i][j]

        for i in range(self.n):
            self.A[i][i] = 0

        self.X = np.random.uniform(0,1, size=(self.n, self.d1))
        self.Theta = np.random.uniform(0,1, size=(self.d1, self.d2))

    def Generate_Random_v2(self):

        self.A = np.full((self.n, self.n), 1)
        UpCnt = 0

        for i in range(self.n):
            self.A[i][i] = 0

        for i in range(self.n-1):
            for j in range(i + 1, self.n):
                UpCnt = UpCnt + 1

        Tmp_test = ((self.n ** 2) - self.n)/2

        if UpCnt != Tmp_test:
            raise Exception("Something really messed up here!!")
        

        self.X = np.random.uniform(0,1, size=(self.n, self.d1))
        self.Theta = np.random.uniform(0,1, size=(self.d1, self.d2))

        Lmt = int(UpCnt *(1-self.fr))

        DwCnt = 0 
        Limit_itr = 0
        while(DwCnt < Lmt and Limit_itr < LIMIT_ITR):

            x = 0
            y = 0

            while (Limit_itr < LIMIT_ITR):

                Limit_itr = Limit_itr + 1

                x = np.random.randint(0, self.n)
                y = np.random.randint(0, self.n)
                
                if x == y or self.A[x][y] == 0:
                    continue
                
                self.A[x][y] = 0
                self.A[y][x] = 0
                self.nedge = self.nedge - 2 
                # ======================================================
                # check if it is still connected or not
                # ======================================================

                # we want to see if we through away x-y edge then the x will be disconnected or not
                # we can access to all nodes with absence of the x-y even going from x to y we will undo the change
                # we are only checking the access of x to other nodes why only x to all other nodes??
                # because the graph was connected before and we are just throwing away x-y edge

                visited = [False] * self.n
                self.DFS(x, visited)
                for b in visited: #if only one member is disconnected we undo the change
                    if not b:
                        self.A[x][y] = 1
                        self.A[y][x] = 1
                        continue

                DwCnt = DwCnt + 1
                break

        

    def DFS(self, v, visited):

        # mark current node as visited
        visited[v] = True
        
        # do for every edge (v, u)
        for u in range(self.n):
            if self.A[v][u] == 1:
                if not visited[u]:
                    self.DFS(u, visited)
    
    def printA(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.A[i][j],end="    ")
            print(" ")

    def check(self):
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                if self.A[i][j] != self.A[j][i]:
                    raise Exception("something is not working right!")
    
    def draw_network(self):
        edgelist = []
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                if self.A[i][j] == 1:
                    edgelist.append((i,j))

        options = {
            'node_color': 'blue',
            'node_size': 100,
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 12,
        }

        G = nx.DiGraph()
        G.add_edges_from(edgelist)
        #nx.draw_networkx(G, arrows=True, **options)
        pos = nx.spring_layout(G, k=0.15, iterations=2)
        nx.draw(G, pos)
        pylab.show() 
    

    def DoTheMath(self):

        self.AA = self.A @ self.A           # n-n . n-n = n by n
        self.AAX = self.AA @ self.X         #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta    #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]   #row of n-d2 = 1 by d2
        self.XT = self.X @ self.Theta       #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() # n-d2 . d2-1 = n-1
        self.Lmt = int(self.nedge * self.FSub)
        
        if self.sr >= self.n or self.sr < 0:
            raise Exception("selected row is not in the range")
        return self.AXTR
    

    def getInfo(self):
        os.system('clear')
        print("===============================================")
        print("===============================================")

        print("%-20s %-15s"%("Number nodes:   ", self.n))
        print("%-20s %-15s"%("Number edges:   ", self.nedge))
        print("%-20s %-15s"%("Target edges:   ", self.Lmt))

        print("=======   Detailed Info  ======================")
        print("%-20s %-15s"%("size of A:   ", self.A.shape))
        print("%-20s %-15s"%("size of X:   ", self.X.shape))
        print("%-20s %-15s"%("size of Theta:   ", self.Theta.shape))
        print("%-20s %-15s"%("size of AA:   ", self.AA.shape))
        print("%-20s %-15s"%("size of AAX:   ", self.AAX.shape))
        print("%-20s %-15s"%("size of AAXT:   ", self.AAXT.shape))
        print("%-20s %-15s"%("size of XT:   ", self.XT.shape))
        print("%-20s %-15s"%("size of AAXTR:   ", self.AAXTR.shape))
        print("%-20s %-15s"%("size of XTW:   ", self.XTW.shape))
        print("===============================================")
        print("===============================================")
        print("===============================================")
    def dump_pickle(self, address):
        out = open(address,'wb')
        tmp_dic = {'A':self.A, 'X':self.X , 'T':self.Theta}
        #pickle.dump(self.A, out)
        #pickle.dump(self.X, out)
        #pickle.dump(self.Theta, out)
        pickle.dump(tmp_dic, out)



        

##  testing part
##  testing part
##  testing part


from arg_pars import ParseArguments
from CreatFile import CreateAdressParseArguments

if __name__ == '__main__':

    # default values
    # to get info about eachone run the code and put -h argument as input to the algorithm
    # you will see all the required information

    N = 10
    D1 = 3
    D2 = 4
    Srow = 2
    Fraction = 0.6
    Condition = 0.5
    TInstance = 10

    args = ParseArguments(N, D1, D2, Srow, Fraction, Condition, TInstance)
    
    N = args.N
    D1 = args.D1
    D2 = args.D2
    Srow = args.SR
    Fraction = args.Fr
    Condition = args.Cn
    TInstance = args.TI
    
    
    for Cnt in range(TInstance):
        
        name , address = CreateAdressParseArguments(N=N, D1= D1, D2=D2, Srow=Srow, Fraction= Fraction, FSub=Condition)
        tt = CreateData(N=N, D1= D1, D2=D2, Srow=Srow, Fraction= Fraction, FSub=Condition)
        tt.Generate_Random_v2()
        tt.DoTheMath()
        tt.dump_pickle(address)
        print("#(%d) file %d is done!"%(Cnt, name))
        del tt

    #print(tt.AXTR)
    #print(tt.AXTR)
    #tt.printA()
    #tt.check()
    #tt.draw_network()