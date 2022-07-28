import numpy as np


A = np.full((3,3), 0, dtype = np.float_)


#   0->1->2
#   0->2

x = 0
y = 1

A[x][y] = 1
A[y][x] = 1


x = 1
y = 2

A[x][y] = 1
A[y][x] = 1


B = A@A
C = B@B
print(B)
print(C)

