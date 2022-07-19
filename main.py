from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result
from draw_graphs import Draw_Picture



def RunMainFuntions():
    St = 254
    Ed = 269
    for x in range(St, Ed):
        InputDt = read_data(x)

        #InputDt.Lmt = int(InputDt.Lmt*0.1)

        #InputDt.show()
        ResultDt = Gurobi_Solve(InputDt)
        print(ResultDt.Time)
        
        #Save data and result
        Write_Result(InputDt, ResultDt)
        Draw_Picture(InputDt, ResultDt)

if __name__ == '__main__':
    RunMainFuntions()
