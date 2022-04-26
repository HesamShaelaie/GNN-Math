import numpy
import pickle

arr = numpy.array([[1, 2], [3, 4]])
arr2 = numpy.array([[5, 6], [3, 4]])
out = open("sample.pkl", "wb")

pickle.dump(arr, out)
pickle.dump(arr2, out)
out.close()
#with open('sample.pkl', 'rb') as f:
with open('/Users/hesamshaelaie/Documents/Research/GNN-Math/GNNINPUT/3.txt', 'rb') as f:
    while True:
        try:
            print(pickle.load(f))
        except EOFError:
            break