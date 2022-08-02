import numpy as np


A = np.full((4,4), 0, dtype = np.float_)


#   0->2->3
#   0->1->3

x = 0
y = 1

A[x][y] = 1


x = 0
y = 2
A[x][y] = 1



x = 2
y = 3
A[x][y] = 1


x = 1
y = 3
A[x][y] = 1


B = A@A
C = B@B
print(B)
print(C)

