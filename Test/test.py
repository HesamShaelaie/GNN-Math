import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print()
a_del = np.delete(a, (0,2), 0)
print(a_del)
# [[ 0  1  2  3]
#  [ 8  9 10 11]]
print()
print(a)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]