import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-tn', dest='N', type=int, default = 20, help='Total number of nodes which create N by N adjacency matrix')
parser.add_argument('-d1', dest='D1', type=int, default = 10, help='Dimension of matrix X which is N by D1')
parser.add_argument('-d2', dest='D2', type=int, default = 15, help='Dimension of matrix theta which is D1 by D2')
parser.add_argument('-sr', dest='SR', type=int, default = 5, help='Selected row in the matrix')
parser.add_argument('-f1', dest='Fr', type=float, default = 0.6, help='Density of the adjacency matrix')
parser.add_argument('-f2', dest='Cn', type=float, default = 0.5, help='Condition of the problem - upper bound on #edges')
parser.add_argument('-ti', dest='TI', type=int, default = 5, help='Total instances to generate')
args = parser.parse_args()

print (str(args))