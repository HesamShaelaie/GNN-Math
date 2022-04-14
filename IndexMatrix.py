import numpy as np


class MatIndex:
    def __init__(self, N):
        self.n = N
        #self.m = M

    def ElementsOf(self, x, y):
        self.B = [(x,i,i,y) for i in range(self.n)]



if __name__ == '__main__':
    tt = MatIndex(N=12)
    tt.ElementsOf(2,4)
    #print(tt.ElementsOf(2,4))
    for X in tt.B:
        print(X[0])
        print(X[1])
        print(X[2])
        print(X[3])
        break
    
