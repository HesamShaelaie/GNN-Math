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
        self.LN = np.empty
        self.On = -1

        self.ERR_A_Diagonal = 0
        self.ERR_A_Symmetry = 0

        for x in range(self.n):
            for y in range(self.n):
                if x==y:
                    if self.A[x,y]!= 0:
                        self.ERR_A_Diagonal = self.ERR_A_Diagonal + 1
                        self.A[x,y] = 0 
                else:
                    if self.A[x,y]>0.5 and self.A[y,x]<0.5:
                        self.ERR_A_Symmetry = self.ERR_A_Symmetry + 1
                        self.A[y,x] = 1
        self.CntA = 0
        for x in range(self.n):
            for y in range(self.n):
                if self.A[x,y]>0.5:
                    self.CntA = self.CntA + 1
        
        if self.DenA%2 != 0:
            print("Input A matrix has problem!")
            exit(3)

        
        if self.ERR_A_Diagonal != 0  or self.ERR_A_Symmetry != 0:
            print("self.ERR_A_Diagonal != 0  or self.ERR_A_Symmetry != 0")
            exit(31)
            
        
        self.DenA = self.CntA/self.n**2 
        self.AA = self.A @ self.A                   #n-n . n-n = n by n
        self.AAX = self.AA @ self.X                 #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta            #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2

        self.tmp_sum = np.full((self.yT, 1), 1, dtype = np.float_)
        self.ObjGNN = self.AAXTR @  self.tmp_sum

        self.XT = self.X @ self.Theta               #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() #n-d2 . d2-1 = n-1
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2
    


    #defualt value of the K is 2 as we got it from the original model
    def recalculate(self, k: int = 2):

        tmp = np.copy(self.A)
        for _ in range(k):
            tmp = tmp @ self.A                   

        self.AA = tmp                               #n-n . n-n = n by n
        self.AAX = self.AA @ self.X                 #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta            #n-d1 . d1-d2 = n by d2
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2

        self.tmp_sum = np.full((self.yT, 1), 1, dtype = np.float_)
        self.ObjGNN = self.AAXTR @  self.tmp_sum

        self.XT = self.X @ self.Theta               #n-d1 . d1-d2 = n by d2
        self.XTW = self.XT @ self.AAXTR.transpose() #n-d2 . d2-1 = n-1
        self.AAXTR = self.AAXT[self.sr,:]           #row of n-d2 = 1 by d2

    def getting_old(self, OA, OP, LN):
        self.OA = OA
        self.OP = OP
        self.On = len(OA[0,:])
        self.LN = LN


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

    def SetNumberQ(self, tmp: np.int16):
        self.NQ = tmp

    def SetTime(self, tmp):
        self.Time = tmp

    def SetX(self, tmp):
        self.X = tmp
    
    def SetObj(self, tmp):
        self.Obj = tmp

    

