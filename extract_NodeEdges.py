from reading_pickles import InputStructure
from reading_pickles import OutputStructure
import os
import csv 

def Write_Node_Edges(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNOUTPUT = CurrectFolder + "/GNNOUTPUT"

    if not os.path.isdir(GNNOUTPUT):
        os.mkdir(GNNOUTPUT)

    general_nodes = GNNOUTPUT +"/Nodes.csv"
    general_edges = GNNOUTPUT +"/Edges.csv"

    if os.path.isfile(general_nodes):
        os.remove(general_nodes)

    if os.path.isfile(general_edges):
        os.remove(general_edges)

    with open(general_nodes, 'w') as f_object:  
        writer = csv.writer(f_object)
        header = ['index',	'sensor_id', 'latitude',	'longitude']
        writer.writerow(header)

    with open(general_edges, 'w') as f_object:  
        writer = csv.writer(f_object)
        header = ['from',	'to']
        writer.writerow(header)
        
    with open(general_nodes, 'a', newline='') as f_object:  

        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)

        for x in range(Input.n):
            Indx = x
            
            Lat = Input.PosID[x][0]
            Log = Input.PosID[x][1]
            IDD = Input.PosID[x][2]
            list_data = [ Indx, IDD, Lat, Log]
            writer.writerow(list_data)

        f_object.close()

    with open(general_edges, 'a', newline='') as f_object:  

        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)

        for x in range(Input.n):
            for y in range(Input.n):
                if Output.X[x][y]>0.5:
                    fr = Input.PosID[x][2]
                    to = Input.PosID[y][2]
                    list_data = [fr, to]
                    writer.writerow(list_data)

        f_object.close()



def Write_Node_Edges_Only(Input: InputStructure, Output: OutputStructure):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNOUTPUT = CurrectFolder + "/GNNOUTPUT"

    if not os.path.isdir(GNNOUTPUT):
        os.mkdir(GNNOUTPUT)

    general_nodes = GNNOUTPUT +"/NodesOnly.csv"
    general_edges = GNNOUTPUT +"/EdgesOnly.csv"

    if os.path.isfile(general_nodes):
        os.remove(general_nodes)

    if os.path.isfile(general_edges):
        os.remove(general_edges)

    with open(general_nodes, 'w') as f_object:  
        writer = csv.writer(f_object)
        header = ['index',	'sensor_id', 'latitude',	'longitude']
        writer.writerow(header)

    with open(general_edges, 'w') as f_object:  
        writer = csv.writer(f_object)
        header = ['from',	'to']
        writer.writerow(header)
        
    with open(general_nodes, 'a', newline='') as f_object:  

        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)
        SetNodes = set()


        for i in range(Input.n):
            for j in range(Input.n):
                if Output.X[i][j] > 0.5:
                    SetNodes.update(set([i]))
                    SetNodes.update(set([j]))


        for x in SetNodes:
            Indx = x
            
            Lat = Input.PosID[x][0]
            Log = Input.PosID[x][1]
            IDD = Input.PosID[x][2]
            
            list_data = [ Indx, IDD, Lat, Log]
            writer.writerow(list_data)

        f_object.close()

    with open(general_edges, 'a', newline='') as f_object:  

        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)

        for x in range(Input.n):
            for y in range(Input.n):
                if Output.X[x][y]>0.5:
                    fr = Input.PosID[x][2]
                    to = Input.PosID[y][2]
                    list_data = [fr, to]
                    writer.writerow(list_data)

        f_object.close()
