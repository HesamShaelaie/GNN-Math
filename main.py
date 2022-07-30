from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result
from draw_graphs import Draw_Picture



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


def RunRealData():
    St = 970003
    Ed = 970004
    for x in range(St, Ed):
        InputDt = read_data(x, INCLUDE_OLD = True)

        InputDt.Lmt = int(InputDt.Lmt * 0.5)

        #InputDt.Lmt = 20*2
        #InputDt.show()
        ResultDt = Gurobi_Solve(InputDt, Lazy=False, YUE=True)
        print(ResultDt.Time)
        print("Problem solved")
        #Save data and result
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt, WithOld=True, YUE= True)


if __name__ == '__main__':
    RunWithOld()