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
>> python data.py -tn 20 -d1 12 -d2 14 -sr 5 -f1 0.4 -f2 0.5 -ti 5

```