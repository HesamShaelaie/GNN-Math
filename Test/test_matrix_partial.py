import numpy as np

np.random.seed(3)



A = np.full((10,10), 10, dtype=float)
CA1 = np.copy
X = np.random.uniform(0,1, size=(10, 20))
T = np.random.uniform(0,1, size=(20, 5))

tmp = np.full((5,1), 1, dtype=float)


AA = A@A
AAX = AA@X
AAXT = AAX@T  #=> 10 by 5

AAXTR = AAXT[0,:] # 1 by 5

Obj = AAXTR@tmp
print(Obj)


