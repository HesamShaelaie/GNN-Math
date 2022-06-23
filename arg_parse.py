
import argparse

import os
import sys

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

def ParseArguments(N, D1, D2, Srow, Fr, Cn, TI):
    parser = argparse.ArgumentParser()
    parser.add_argument('-tn', dest='N', type=int, default = N, help='Total number of nodes which create N by N adjacency matrix')
    parser.add_argument('-d1', dest='D1', type=int, default = D1, help='Dimension of matrix X which is N by D1')
    parser.add_argument('-d2', dest='D2', type=int, default = D2, help='Dimension of matrix theta which is D1 by D2')
    parser.add_argument('-sr', dest='SR', type=int, default = Srow, help='Selected row in the matrix')
    parser.add_argument('-f1', dest='Fr', type=float, default = Fr, help='Density of the adjacency matrix')
    parser.add_argument('-f2', dest='Cn', type=float, default = Cn, help='Condition of the problem - upper bound on #edges')
    parser.add_argument('-ti', dest='TI', type=int, default = TI, help='Total instances to generate')
    args = parser.parse_args()


    os.system('clear')
    print("=========================================================")
    print("=========================================================")
    print(str(args))
    print("=========================================================")
    print("=========================================================\n")

    print("Press y to continue and any other key to exit!")
    c = wait_key()
    if c=='y':
        os.system('clear')
        return args
    else:
        exit(23)

if __name__ == '__main__':
    
    N = 20
    D1 = 10
    D2 = 15
    Srow = 3
    Fraction = 0.5
    Condition = 0.5
    TInstance = 10

    args = ParseArguments(N, D1, D2, Srow, Fraction, Condition, TInstance)
    print(args.N)
    print(str(args))