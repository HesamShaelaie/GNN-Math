from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result
from draw_graphs import Draw_Picture
import numpy as np


def RunMainFuntions():
    
    St = 254
    Ed = 255
    
    for x in range(St, Ed):

        InputDt = read_data(x)
        #InputDt.A = InputDt.A @ InputDt.A
        #InputDt.recalculate()

        #InputDt.Lmt = int(InputDt.Lmt*0.2)

        print('InputDt.Lmt:     %d'%InputDt.Lmt)
        print('InputDt.CntA:    %d'%InputDt.CntA)
        
        ResultDt = Gurobi_Solve(InputDt)
        print(ResultDt.Time)
        
        #Save data and result
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt)



def RunWithOld():
    
    St = 70254
    Ed = 70255
    for x in range(St, Ed):
        InputDt = read_data(x, INCLUDE_OLD = True)

        InputDt.Lmt = int(InputDt.Lmt * 0.5)
        InputDt.Lmt = 20*2
        #InputDt.show()
        ResultDt = Gurobi_Solve(InputDt)
        print(ResultDt.Time)
        print("Problem solved")
        #Save data and result
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt, WithOld=True)



#pems-bay-K=5-directed-A 900004
#metr-la-K=5-directed-A 900005
#pems-bay-K=5-directed-A-sensor-id 900006

def RunRealData():

    St = 900003
    Ed = 900004

    for x in range(St, Ed):

        InputDt = read_data(x, INCLUDE_OLD = False, YUE=True)
        
        InputDt.X = np.full((InputDt.xX, InputDt.yX), 1, dtype = np.float_)
        InputDt.Theta = np.full((InputDt.xT, InputDt.yT), 1, dtype = np.float_)

        InputDt.recalculate(1, ResetLimit = True)
        
        InputDt.Lmt = int(InputDt.Lmt * 0.5)

        ResultDt = Gurobi_Solve(InputDt, Lazy=False, YUE=True, Testing= False)

        print(ResultDt.Time)
        print("Problem solved")
        
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt, WithOld=False, YUE= True)


if __name__ == '__main__':
    RunRealData()