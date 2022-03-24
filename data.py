import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab

LIMIT_ITR = 10000
class CreateData:

    def __init__(self, N, D1, D2, Srow, Fraction):
        self.n = N
        self.d1 = D1
        self.d2 = D2
        self.sr = Srow
        self.fr = Fraction

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


        self.X = np.random.uniform(0,1, size=(self.n, self.d1))
        self.Theta = np.random.uniform(0,1, size=(self.d1, self.d2))
        Lmt = int(UpCnt *(1-self.fr))

        DwCnt = 0 
        Limit_itr = 0
        while(DwCnt < Lmt and Limit_itr<LIMIT_ITR):

            x = 0
            y = 0

            while (Limit_itr < LIMIT_ITR):

                Limit_itr = Limit_itr + 1

                x = np.random.randint(0,self.n)
                y = np.random.randint(0,self.n)
                
                if x == y or self.A[x][y] == 0:
                    continue
                
                self.A[x][y] = 0
                self.A[y][x] = 0

                visited = [False] * self.n
                self.DFS(x, visited)
                for b in visited:
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
        

if __name__ == '__main__':

    tt = CreateData(20, 11, 12, 13, 0.3)
    tt.Generate_Random_v2()
    tt.printA()
    tt.check()
    tt.draw_network()



