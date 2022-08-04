import numpy as np


class InputStructure():
    def __init__(self,Index,Path, Fname, A, X, T, R, L, P) -> None:
        self.Index = Index

        self.n = np.shape(A)[0]

        self.xA = np.shape(A)[0]
        self.yA = np.shape(A)[1]

        self.xT = np.shape(T)[0]
        self.yT = np.shape(T)[1]

        self.xX = np.shape(X)[0]
        self.yX = np.shape(X)[1]    

        if(self.xA != self.yA):
            print("self.xA != self.yA")
            exit(33)

        if(self.yA != self.xX):
            print("self.yA != self.xX")
            exit(33)

        if(self.yX != self.xT):
            print("self.yX != self.xT")
            exit(33)
        

        
        
        self.A = any
        if type(A[0][0]==bool):
            self.A = np.full((self.n, self.n), 0, dtype = np.float_)
            for x in range(self.n):
                for y in range(self.n):
                    if A[x][y] == True:
                        self.A[x][y]=1
        else:
            self.A = A
        
        for x in range(self.n):
            A[x][x] = 0

        self.CopyA = np.copy(self.A)
        self.CopyX = np.copy(X)
        self.CopyTheta = np.copy(T)

        
        self.X = X
        self.Theta = T
        self.sr = R
        self.Lmt = L
        self.DenAO = 0.0
        self.Path = Path
        self.Fname = Fname
        self.Pos = P

        self.OriginalA = np.empty
        self.OA = np.empty
        self.OP = {}
        self.LN = np.empty
        self.On = -1
        self.K = -1 

        self.CntAO = 0
        for x in range(self.n):
            for y in range(self.n):
                if self.CopyA[x][y]>0.5:
                    self.CntAO = self.CntAO + 1

        self.DenAO = float(self.CntAO*100)/self.n**2 
    

    def reset_A(self):
        self.A = np.copy(self.CopyA)

    def set_A(self, tmp):
        self.A = tmp
    
    def blank_X(self):
        self.X = np.full((self.xX, self.yX), 1, dtype = np.float_)
        
    def blank_T(self):
        self.Theta = np.full((self.xT, self.yT), 1, dtype = np.float_)

    def reset_X(self):
        self.X = np.copy(self.CopyX)

    def reset_T(self):
        self.Theta = np.copy(self.CopyTheta)

    #defualt value of the K is 2 as we got it from the original model
    def recalculate(self, K: int = 1, ResetLimit:bool = True, WithAdjustment:bool = True):

        tmp = np.copy(self.A)

        self.K = K

        for _ in range(1, K):
            tmp = tmp @ self.A

        if WithAdjustment:
            for x in range(self.n):
                tmp[x][x] = 0

        self.A = tmp
        self.AA = self.A @ self.A                   #n-n . n-n = n by n
        self.AAX = self.AA @ self.X                 #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta            #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2

        self.tmp_sum = np.full((self.yT, 1), 1, dtype = np.float_)
        self.ObjGNN = self.AAXTR @  self.tmp_sum

        self.XT = self.X @ self.Theta               #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() #n-d2 . d2-1 = n-1
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2
        
        self.CntAK = 0
        for x in range(self.n):
            for y in range(self.n):
                if self.A[x][y]>0.5:
                    self.CntAK = self.CntAK + 1

        self.DenAK = float(self.CntAK*100)/self.n**2

        if ResetLimit:
            self.Lmt = self.CntAK

        
    def getting_old(self, OA, OP, LN, OriginalA):
        self.OA = OA
        self.OP = OP
        self.On = len(OA[0,:])
        self.LN = LN
        self.OriginalA = OriginalA

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
        self.ObjMO = 0.0
        self.Time =0.0
        self.CntX = 0

    def SetNumberQ(self, tmp: np.int16):
        self.NQ = tmp

    def SetTime(self, tmp):
        self.Time = tmp

    def SetX(self, tmp):
        self.X = tmp
    
    def SetObj(self, tmp):
        self.Obj = tmp

    

