from ctypes import sizeof
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os
import pickle
import sys
import math
from datetime import datetime
import random

now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
print("date and time =", dt_string)	

LIMIT_ITR = 100000

class CreateData:

    def __init__(self, N, D1, D2, Srow, Fraction, FSub=-1):
        self.n = N
        self.d1 = D1
        self.d2 = D2
        self.sr = Srow
        self.fr = Fraction
        self.AXT = np.empty
        self.AXTR = np.empty
        self.nedge = N*(N-1)
        self.FSub = FSub
        self.Pos = np.empty

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
        
        self.Pos = np.random.randint(0,2000, size=(self.n, 2))


        self.A = np.full((self.n, self.n), 1, dtype = np.float_)
        UpCnt = 0

        for i in range(self.n):
            self.A[i][i] = 0

        for i in range(self.n-1):
            for j in range(i + 1, self.n):
                UpCnt = UpCnt + 1

        Tmp_test = ((self.n ** 2) - self.n)/2

        if UpCnt != Tmp_test or (Tmp_test*2)!= self.nedge:
            raise Exception("UpCnt != Tmp_test or (Tmp_test*2)!= self.nedge")
        

        self.X = np.random.uniform(0,1, size=(self.n, self.d1))
        self.Theta = np.random.uniform(0,1, size=(self.d1, self.d2))

        Lmt = int(UpCnt *(1-self.fr)) # we should delete this number

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

                visited = np.full(self.n, 0, dtype = np.bool_)
                self.DFS_Nonrecursive(x, visited)
                for b in visited: #if only one member is disconnected we undo the change
                    if not b:
                        self.A[x][y] = 1
                        self.A[y][x] = 1
                        break
                
                if self.A[x][y] == 0:
                    DwCnt = DwCnt + 1
                    break
    

    def Generate_Random_v3(self):
        
        numberPoints = self.n

        Lw = 0
        Hw = 800
            
        Lh = 0
        Hh = 600

        adjusting_space = 0.9
        Limit_space = (float(Hw-Lw) * float(Hh-Lh)* adjusting_space)/numberPoints
        Limit_distance = math.sqrt((Limit_space/3.14))
            
        MidW = (Lw + Hw)/2
        MidH = (Lh + Hh)/2

        itr = 0
        itr_s = 0
        itr_limit = 5000000

        dist = -0.0
        find = False
        points = {}

        while(itr < numberPoints and itr_s< itr_limit):

            tmp_node = [random.uniform(Lw, Hw), random.uniform(Lh, Hh)]
            find = False
            for key, value in points.items():

                x = (tmp_node[0]-value[0])**2
                y = (tmp_node[1]-value[1])**2
                z = x + y
                dist = math.sqrt(z)

                if (dist < Limit_distance):
                    find = True
                    break
            
            if (not find):
                points.update({itr:tmp_node})
                itr = itr +1 
            
            itr_s = itr_s + 1


        if (itr_s == itr_limit):

            print("cannot creat the instance!!")
            exit(2)

        tmp_pos = []
        for x in range(self.n):
            tmp_pos.append(points[x])

        self.Pos = tmp_pos

        print("Positions => done")
        from scipy.spatial import Delaunay
        tri = Delaunay(tmp_pos)
        print("Delaunay => done")
        #print(tri.simplices)
        
        # finding the center 
        min_k = -1
        min_v = 999999999.0

        for key, value in points.items():
                
            
            x = (MidW-value[0])**2
            y = (MidH-value[1])**2
            z = x + y
            dist = math.sqrt(z)
            if (dist < min_v):
                min_v = dist
                min_k = key

        print("Found the row => done")        
        self.sr = min_k

        # extracting the edges
        edge_list = []
        for tri in tri.simplices:
            edge_list.append([tri[0], tri[1]])
            edge_list.append([tri[1], tri[2]])
            edge_list.append([tri[2], tri[0]])

        print("Extract the edge => done")
        self.A = np.full((self.n, self.n), 0, dtype = np.float_)
        for x in edge_list:
            a = x[0]
            b = x[1]
            self.A[a][b] = 1
            self.A[b][a] = 1
        

        UpCnt = 0
        for x in range(self.n):
            for y in range(x,self.n):
                if(self.A[x][y]>0.5):
                    UpCnt = UpCnt + 1
        

        print("Counted the edge => done")
        self.nedge = UpCnt
        self.X = np.random.uniform(0,1, size=(self.n, self.d1))
        self.Theta = np.random.uniform(0,1, size=(self.d1, self.d2))

        print("Genrated the x theta => done")

        Lmt = int(UpCnt *(1-self.fr)) # we should delete this number
        print("Org #edge: %d and reduction is %d:"%(UpCnt, Lmt),end="    ",flush=True)
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

                visited = np.full(self.n, 0, dtype = np.bool_)
                self.DFS_Nonrecursive(x, visited)
                for b in visited: #if only one member is disconnected we undo the change
                    if not b:
                        self.A[x][y] = 1
                        self.A[y][x] = 1
                        self.nedge = self.nedge + 2
                        break
                
                if self.A[x][y] == 0:
                    DwCnt = DwCnt + 1
                    print(",%d"%(DwCnt),end="",flush=True)
                    break
        

        print("!!!",end="   ")
        if Limit_itr == LIMIT_ITR:
            print("")
            print("error: Limit_itr == LIMIT_ITR!!!")
            exit(123)
    
    def distance(A , B):

        x = (A[0]-B[0])**2
        y = (A[1]-B[1])**2
        z = x + y
        return math.sqrt(z)
        

    def DFS_recursive(self, v, visited):

        # mark current node as visited
        visited[v] = True
        
        # do for every edge (v, u)
        for u in range(self.n):
            if self.A[v][u] == 1:
                if not visited[u]:
                    self.DFS_recursive(u, visited)

    def DFS_Nonrecursive(self, v, visited):

        # Mark current node as visited
        
        Clist = np.zeros(self.n, dtype=np.int16)
        Clist[0] = v
        cnt = 1

        while cnt > 0:
            v = Clist[cnt-1]
            cnt = cnt - 1 
        # do for every edge (v, u)
            for u in range(self.n):
                if self.A[v][u] == 1:
                    if not visited[u]:
                        Clist[cnt] = u
                        cnt = cnt + 1
                        visited[u] = True
    
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

        if  self.nedge < self.Lmt:
            print("some problem in do the math!!")
            exit(12)

        
        print("#edge: %d - #Lmt: %d"%(self.nedge, self.Lmt))
        if self.sr >= self.n or self.sr < 0:
            raise Exception("selected row is not in the range")
        return self.nedge, self.Lmt
            
    

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
        tmp_dic = {'A':self.A, 'X':self.X , 'T':self.Theta, 'R': self.sr, 'L':self.Lmt, 'P':self.Pos}
        #pickle.dump(self.A, out)
        #pickle.dump(self.X, out)
        #pickle.dump(self.Theta, out)
        pickle.dump(tmp_dic, out)
        out.close()

##  testing part
##  testing part
##  testing part

from arg_parse import ParseArguments
from create_file import CreateAdressParseArguments

if __name__ == '__main__':

    # Default values
    # to get info about eachone run the code and put -h argument as input to the algorithm
    # you will see all the required information

    N = 50
    D1 = 5
    D2 = 5
    Srow = 2
    Fraction  = 0.95        #it should be between zero and one
    Condition = 1.0         #it should be between zero and one
    TInstance = 10          #number of instances generated

    args = ParseArguments(N, D1, D2, Srow, Fraction, Condition, TInstance)
    
    N = args.N
    D1 = args.D1
    D2 = args.D2
    Srow = args.SR
    Fraction = args.Fr
    Condition = args.Cn
    TInstance = args.TI
    
    for Cnt in range(TInstance):
        
        
        tt = CreateData(N=N, D1= D1, D2=D2, Srow=Srow, Fraction= Fraction, FSub=Condition)
        tt.Generate_Random_v3()
        Nedge, Nlimit = tt.DoTheMath()

        name , address = CreateAdressParseArguments(N= N, D1= D1, D2= D2, Srow= Srow, Fraction= Fraction, FSub= Condition,Nedge=Nedge, Lmt= Nlimit)
        tt.dump_pickle(address)
        print("#(%d) file %d is done!"%(Cnt, name))
        del tt

    #print(tt.AXTR)
    #print(tt.AXTR)
    #tt.printA()
    #tt.check()
    #tt.draw_network()