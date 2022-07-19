import os 
import os.path
from datetime import datetime

def CreateAdressParseArguments(N, D1, D2, Srow, Fraction, FSub, Nedge, Lmt):
    CurrectFolder = os.getcwd()
    GNNINPUT = CurrectFolder + "/GNNINPUT"

    #print(GNNINPUT)
    if not os.path.isdir(GNNINPUT):
        os.mkdir(GNNINPUT)

    Add_general_info = GNNINPUT +"/GeneralInfo.txt"

    LastFileNumber = -1
    if os.path.isfile(Add_general_info):

        with open(Add_general_info, 'r') as fopen:
            last_line = fopen.readlines()[-1]
            last_line = last_line.split()
            LastFileNumber = int(last_line[0]) + 1
            fopen.close()
            

    else:
        open(Add_general_info, 'w').close()
        LastFileNumber = 0
    
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    #print("date and time =", dt_string)

    out = open(Add_general_info, "a")
    out.write("%4d  %s     N<-%4d D1<-%4d  D2<-%4d SR<-%4d Fr <-%.2f Cn <-%.2f edge  <- %d  Lim  <-  %d\n"%(LastFileNumber, dt_string, N, D1, D2, Srow, Fraction, FSub, Nedge, Lmt))
    out.close()
    return LastFileNumber, "%s/%d.txt"%(GNNINPUT ,LastFileNumber)

if __name__ == '__main__':

    N = 20
    D1 = 10
    D2 = 15
    Srow = 3
    Fraction = 0.5
    Condition = 0.5

    LF = CreateAdressParseArguments(N, D1, D2, Srow, Fraction, Condition)

    print(LF)
    exit(10)




