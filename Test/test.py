NodeNotInList = [2 ,6]
ALLNode = [x for x in range(10)]

for t in NodeNotInList:
    for y in range(10):
        if t == y:
            ALLNode[y] = -1
        elif t < y:
            ALLNode[y] = ALLNode[y]-1

print(ALLNode)