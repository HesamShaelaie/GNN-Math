import pickle
import os
from matplotlib.font_manager import findSystemFonts
import numpy as np
from numpy import empty 
from data_structures import InputStructure
from data_structures import OutputStructure

#{'A':engine.model.A, 'A_POW':engine.model.A_pow, 'X': dataloader['val_loader'].xs,  'T':engine.model.theta, 'R':0, 'L':0, 'lat': engine.model.lat, 'lng': engine.model.lng}

def read_data(Index, INCLUDE_OLD = False, YUE=False):
    
    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNINPUT = CurrectFolder + "/GNNINPUT/"

    print("reading the file %d!!"%(Index))
    Fname = "%d"%(Index)
    path_to_file = "%s%d.txt"%(GNNINPUT, Index)
    Fresult= os.path.exists(path_to_file)

    if Fresult == False:
        raise Exception('Cannot read the file!!')

    with open(path_to_file, 'rb') as f:
        try:
            Info =pickle.load(f)
        except EOFError:
            raise Exception("cannot read the content!!")
        f.close()

    A = Info['A']
    X = Info['X']
    T = Info['T']
    R = Info['R']
    L = Info['L']

    lng = empty
    lat = empty

    P   = {}
    if YUE == True:
        lng = Info['lng']
        lat = Info['lat']
        for i, (lh, lw) in enumerate(zip(lat, lng)):
            P.update({i:[lh,lw]})
    

        tmpA = np.shape(A)[0]

        for x in range(tmpA):
            for y in range(tmpA):
                if A[x][y]>0.5:
                    A[x][y]=1
                    A[y][x]=1


        for x in range(tmpA):
            A[x][x]=0

        print(np.shape(X))
        tmpX = X[0,:,:,0].transpose()
        X = tmpX

    else:
        P = Info['P']

    n = len(A[0,:])
    cnt = 0
    for x in range(n):
        for y in range(n):
            if A[x,y]>0.5:
                cnt = cnt + 1
    
    if cnt < L:
        print("something is wrong with input!!")
        exit(12)


    InputDt = InputStructure(Index, path_to_file, Fname, A, X, T, R, L, P)

    if INCLUDE_OLD:
        InputDt.getting_old(OA= Info['OA'], OP= Info['OP'], LN=Info['LN'])

    return InputDt

if __name__ == '__main__':
    
    InputDt = read_data(900003, INCLUDE_OLD = False, YUE = True)
    

    #InputDt.show()



