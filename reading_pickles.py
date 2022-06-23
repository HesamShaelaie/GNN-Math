import pickle
import os 
from data_structures import InputStructure


def read_data(Index):
    
    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNINPUT = CurrectFolder + "/GNNINPUT/"

    print("reading the file %d!!"%(Index))
    Fname = "%d.txt"%(Index)
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

    InputDt = InputStructure(Index, path_to_file, Fname, A, X, T, R, L)

    return InputDt

if __name__ == '__main__':
    InputDt = read_data(15)
    InputDt.show()


        