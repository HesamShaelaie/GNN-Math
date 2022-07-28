import numpy as np

epz = 0.0000001

def compare_matrix_g(A, B):
    SizeA = np.shape(A)
    SizeB = np.shape(B)

    if SizeA!=SizeB:
        print('SizeA!=SizeB')
        exit(1)

    if len(SizeA) == 2:
        for x in range(SizeA[0]):
            for y in range(SizeA[1]):
                if A[x][y]+epz< B[x][y]:
                    print('A[%d][%d]=%f'%(x,y,A[x][y]))
                    print('B[%d][%d]=%f'%(x,y,B[x][y]))
                    return False
        
        return True

    elif len(SizeA) == 1:
        for x in range(SizeA[0]):
            if A[x]+epz< B[x]:
                print('A[%d]=%f'%(x,A[x]))
                print('B[%d]=%f'%(x,B[x]))
                return False
        
        return True
    else:
        print('size problem!!')
        exit(33)