# GNN-Math

## data.py
In order to create data you just need to run data.py with the default values in the file for the following variables:

| Variable | Argument | Description  | Default value  |
| :---:   | :-: | :-: | :-: |
| n | -tn | Total number of nodes which create N by N adjacency matrix | 10 |
| d1 | -d1 | Dimension of matrix X which is N by D1 | 3 |
| d2 | -d2 | Dimension of matrix theta which is D1 by D2 | 4 |
| sr | -sr | Selected row in the matrix | 2 |
| fr | -f1 | Density of the adjacency matrix | 0.6 |
| cn | -f2 | Condition of the problem - upper bound on #edges | 0.5 |
| ti | -ti | Total instances to generate | 10 |


You can change default values by the following command:
```
>> python3 data.py -tn 20 -d1 12 -d2 14 -sr 5 -f1 0.4 -f2 0.5 -ti 5
```

output:
```
=========================================================
=========================================================
Namespace(N=20, D1=12, D2=14, SR=5, Fr=0.4, Cn=0.3, TI=5)
=========================================================
=========================================================

Press y to continue and any other key to exit!
```
You can use the help to get brief information on each arg:
```
>> python3 data.py -h
```
You will find the generated data in the folder "GNNINPUT". Input data are named by increasing integer values, but you can find detailed information on each file in the "GeneralInfo.txt".

Content of each pickle is a dictionary with keys of

| Key | Description | Size |
| :---: | :-: | :-: |
| A |  Adjacency matrix | n by n | 
| X | Feature matrix | n by d1 |
| T | Converting matrix | d1 by d2 |
| R | Selected node | 1 by 1 |
| L | Upper bound on number of edges | 1 by 1 |
