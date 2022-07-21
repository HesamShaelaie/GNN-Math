import numpy as np


class InputStructure():
    def __init__(self,Index,Path, Fname, A,X,T,R,L,P) -> None:
        self.Index = Index
        self.n = len(A[0,:])
        self.A = A
        self.X = X
        self.Theta = T
        self.sr = R
        self.Lmt = L
        self.DenA = 0.0
        self.Path = Path
        self.Fname = Fname
        self.Pos = P

        self.OA = np.empty
        self.OP = {}
        self.On = -1


        for x in range(self.n):
            for y in range(self.n):
                if self.A[x,y]>0.5:
                    self.DenA = self.DenA + 1

        if self.DenA%2 != 0:
            print("Input A matrix has problem!")
            exit(3)
        
        self.DenA = self.DenA/self.n**2 
        self.AA = self.A @ self.A           # n-n . n-n = n by n
        self.AAX = self.AA @ self.X         #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta    #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]   #row of n-d2 = 1 by d2
        self.XT = self.X @ self.Theta       #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() # n-d2 . d2-1 = n-1

    def getting_old(self, OA, OP):
        self.OA = OA
        self.OP = OP
        self.On = len(OA[0,:])


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
    
    def __init__(self) -> None:
        self.NQ = 0
        self.Obj =0.0
        self.X = any
        self.Time =0.0

    def SetNumberQ(self, tmp: np.int16):
        self.NQ = tmp

    def SetTime(self, tmp):
        self.Time = tmp

    def SetX(self, tmp):
        self.X = tmp
    
    def SetObj(self, tmp):
        self.Obj = tmp

    

