import numpy as np


A = np.full((4,4), 0, dtype = np.float_)


#   0->1->2->3
#   0->2->3

x = 0
y = 1

A[x][y] = 1
A[y][x] = 1


x = 1
y = 2

A[x][y] = 1
A[y][x] = 1


x = 2
y = 3

A[x][y] = 1
A[y][x] = 1



x = 0
y = 2

A[x][y] = 1
A[y][x] = 1


x = 2
y = 3

A[x][y] = 1
A[y][x] = 1


print(A@A)
