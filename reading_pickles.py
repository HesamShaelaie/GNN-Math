import pickle
import os
from matplotlib.font_manager import findSystemFonts
import numpy as np
from numpy import empty 
from data_structures import InputStructure
from data_structures import OutputStructure

#{'A':engine.model.A, 'A_POW':engine.model.A_pow, 'X': dataloader['val_loader'].xs,  'T':engine.model.theta, 'R':0, 'L':0, 'lat': engine.model.lat, 'lng': engine.model.lng}

def read_data(Index, INCLUDE_OLD = False, YUE=False, INCLUDE_ID = False):
    
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

    lng = empty
    lat = empty

    P = {}
    P_ID = {}
    if YUE == True:
        lng = Info['lng']
        lat = Info['lat']
        IDD = Info['sensor_id']
        for i, (lh, lw, ld) in enumerate(zip(lat, lng, IDD)):
            P.update({i:[lh,lw]})
            P_ID.update({i:[lh,lw,ld]})
    
        tmpA = np.shape(A)[0]
        CntAm = 0
        for x in range(tmpA):
            for y in range(tmpA):
                if A[x][y]>0.5:
                    CntAm = CntAm + 1
                
        print(np.shape(X))
        tmpX = X[0,:,:,0].transpose()

        X = tmpX
        L = CntAm

    else:
        P = Info['P']
        L = Info['L']

    n = len(A[0,:])
    cnt = 0
    for x in range(n):
        for y in range(n):
            if A[x][y]>0.5:
                cnt = cnt + 1
    
    if cnt < L:
        print("something is wrong with input!!")
        exit(12)


    InputDt = InputStructure(Index, path_to_file, Fname, A, X, T, R, L, P)

    if INCLUDE_ID:
        InputDt.GetID(P_ID)

    if INCLUDE_OLD:
        InputDt.getting_old(OA= Info['OA'], OP= Info['OP'], LN=Info['LN'], OriginalA=Info['ORGA'])

    return InputDt


if __name__ == '__main__':
    InputDt = read_data(254, INCLUDE_OLD = False, YUE = False)

    CntA = 0
    CntB = 0
    for x in range(InputDt.n):
        for y in range(InputDt.n):
            if InputDt.A[x][y]>0.5:
                CntA = CntA + 1
    
    for x in range(InputDt.n):
        for y in range(InputDt.n):
            if InputDt.A[x, y]>0.5:
                CntB = CntB + 1
    
    print(CntA)
    print(CntB)

    #InputDt.show()



