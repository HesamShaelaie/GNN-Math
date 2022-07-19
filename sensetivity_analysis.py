from reading_pickles import read_data
import os
import pickle



index = 156
After = 5000
limits = [float(x/100) for x in range(100,30,-2)]

CurrectFolder = os.path.dirname(os.path.abspath(__file__))
GNNINPUT = CurrectFolder + "/GNNINPUT"

InputDt = read_data(index)
box = InputDt.Lmt

for x in range(After, After + len(limits)):

    # checking the limit on the input file
    print("Limit presentage is %d"%(limits[x-After]*100),end="  ")

    InputDt.Lmt = int(box*limits[x-After])

    print("is %d edges"%(InputDt.Lmt), end="    ")


    # creating its address
    address = "%s/%d.txt"%(GNNINPUT ,x)

    # delete if file exists
    if os.path.exists(address):
        os.remove(address)
    
    # dump the information
    out = open(address,'wb')
    tmp_dic = {'A':InputDt.A, 'X':InputDt.X , 'T':InputDt.Theta, 'R': InputDt.sr, 'L':InputDt.Lmt, 'P':InputDt.Pos}
    pickle.dump(tmp_dic, out)
    out.close()

    # print it is done now
    print(" =>  done!")
     