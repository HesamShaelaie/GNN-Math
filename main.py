from reading_pickles import InputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result

def RunMainFuntions():
    St = 25
    Ed = 28
    for x in range(St, Ed):
        InputDt = read_data(x)

        #InputDt.show()
        ResultDt = Gurobi_Solve(InputDt)
        print(ResultDt.Time)
        #Save data and result
        Write_Result(InputDt, ResultDt)

if __name__ == '__main__':
    RunMainFuntions()
