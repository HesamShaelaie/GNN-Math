import numpy as np


class InputStructure():
    def __init__(self,Index, A,X,T,R,L) -> None:
        self.Index = Index
        self.n = len(A[0,:])
        self.A = A
        self.X = X
        self.Theta = T
        self.sr = R
        self.Lmt = L

        self.AA = self.A @ self.A           # n-n . n-n = n by n
        self.AAX = self.AA @ self.X         #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta    #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]   #row of n-d2 = 1 by d2
        self.XT = self.X @ self.Theta       #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() # n-d2 . d2-1 = n-1

    def show(self):
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



class OutputStructure():
    
    def SetNumberQ(self, tmp: np.int16):
        self.NQ = tmp

    def SetTime(self, tmp):
        self.Time = tmp

    def SetX(self, tmp):
        self.X = tmp
    
    def SetObj(self, tmp):
        self.Obj = tmp

    

