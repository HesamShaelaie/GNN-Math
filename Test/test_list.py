TestList = []


TestList.append((1,2))

i = 2
j = 1
if (i,j) not in TestList and (j,i) not in TestList:
    TestList.append((i,j))


print(TestList)