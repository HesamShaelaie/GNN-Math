import pickle
import os 
from data_structures import InputStructure
from data_structures import OutputStructure


def read_data(Index, INCLUDE_OLD = False):
    
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
        InputDt.getting_old(OA= Info['OA'], OP= Info['OP'])

    return InputDt

if __name__ == '__main__':
    InputDt = read_data(15)
    InputDt.show()


        