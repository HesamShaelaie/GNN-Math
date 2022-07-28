import numpy as np

epz = 0.0000001

def compare_matrix_g(A, B):
    SizeA = np.shape(A)
    SizeB = np.shape(B)

    if SizeA!=SizeB:
        print("SizeA!=SizeB")
        exit(1)

    for x in range(SizeA[0]):
        for y in range(SizeA[1]):
            if A[x][y]+epz< B[x][y]:
                print('A[%d][%d]=%f'%(x,y,A[x][y]))
                print('B[%d][%d]=%f'%(x,y,B[x][y]))
                return False
    
    return True


if __name__ == '__main__':

    A = np.full((100,100), 1, dtype = np.float_)

    for _ in range(100):
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        A[x][y] = 0 

    
    B = np.copy(A)

    for _ in range(100):
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        B[x][y] = 0 

    print(compare_matrix_g(A,B))

    tmpA = A@A
    tmpB = B@B
    print(compare_matrix_g(tmpA,tmpB))




