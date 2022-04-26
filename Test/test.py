



#z = [(i,i+1,i+2) for i in range(10)]


#for a, b, c in z:
#    print("%5d %5d %5d"%(a , b, c))




import numpy as np
np.random.seed(2021)


A = np.random.randint(0,10, size=(10, 10))
C = np.random.randint(0,10, size=(10, 7))

B = A@A
D = B@C

F = D[0,:]



T = A[0,:]@A
DD = T@C

print(F)
print(DD)