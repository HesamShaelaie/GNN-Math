import pickle
import os 

CurrectFolder = os.getcwd()
GNNINPUT = CurrectFolder + "/GNNINPUT/"


for x in range(15,16):

    print("reading the file %d!!"%(x))
    path_to_file = "%s%d.txt"%(GNNINPUT,x)
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

    #print(A[1:4,1:4])
    #print(L)


        