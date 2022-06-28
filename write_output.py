from data_structures import InputStructure
from data_structures import OutputStructure
import os
from datetime import datetime

import csv 

def Write_Result(Input: InputStructure, Output: OutputStructure):
    # general info

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNOUTPUT = CurrectFolder + "/GNNOUTPUT"

    #print(GNNINPUT)
    """
    if not os.path.isdir(GNNINPUT):
        os.mkdir(GNNINPUT)

    Add_general_info = GNNINPUT +"/GeneralInfo.txt"

    
    if not os.path.isfile(Add_general_info):
        open(Add_general_info, 'w').close()
    

    FileNumber = Input.Index
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    #print("date and time =", dt_string)

    out = open(Add_general_info, "a")
    out.write("%4d  %s     N<-%4d D1<-%4d  D2<-%4d SR<-%4d Fr <-%.2f Cn <-%.2f\n"%(FileNumber, dt_string, N, D1, D2, Srow, Fraction, FSub))
    out.close()
    return LastFileNumber, "%s/%d.txt"%(GNNINPUT ,LastFileNumber)
    """

    if not os.path.isdir(GNNOUTPUT):
        os.mkdir(GNNOUTPUT)

    general_info = GNNOUTPUT +"/GeneralInfo.csv"

    if not os.path.isfile(general_info):

         with open(general_info, 'w') as f_object:  
            writer = csv.writer(f_object)
            header = ['name', 'Time', 'Duration', 'Obj', '#Q', 'Size-A','Den-A','Lim','Size-X-x','Size-X-y', 'Size-T-x', 'Size-T-y', 'R']
            writer.writerow(header)
            
    
    
    # Pre-requisite - The CSV file should be manually closed before running this code.
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
    with open(general_info, 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)
        # Result - a writer object
        print(Output.Time)
        list_data = [Input.Index, dt_string, Output.Time, Output.Obj, Output.NQ, Input.n, Input.DenA, Input.Lmt, len(Input.X[:,0]),  len(Input.X[0,:]), len(Input.Theta[:,0]), len(Input.Theta[0,:]), Input.sr]
        writer.writerow(list_data)  
        # Close the file object
        f_object.close()

    # check if the general info exist if
    # create folder
    # create the file
    # put it there
    # close the file


    # details

