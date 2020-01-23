# The analysis of experimental data results of my lab

The purpose of this project is to organize the data and convert it to the format needed to facilitate analysis.

this project needs Python 3 and Pandas, have to isntall these packages:

```
pip3 install pandas
```

for Mac user:

```
pip3 install pandas --user 
```

## Execute and generate summary result

Before generate these summary result csv, make sure put all of tester data in `data_source` folder, the folder structure will looks:

```
./data_source

├── tester1
│   ├── 1-A-1.csv
│   ├── 1-A-2.csv
│   ├── 1-A-3.csv
│   ├── 2-E-1.csv
│   ├── ...
```

also make sure each csv file name are correct format: `[1-9]-[A-I]-[1-3]).csv`.

After all files in data_source prepare well, run:

```
python3 combine_with_loop.py -i <totalUserCnunt>
```

or

```
./combine_with_loop.py -i <totalUserCnunt>
```

The script will calculate the average of three data sets from each English alphabet group(A-I) by each tester, then create summary result csv in each ./data_source/tester{N}/summary/summary_tester{N}.csv.

The example result of summary file:

```
  Att_0s_avg Att_1s_avg Att_2s_avg Med_0s_avg Med_1s_avg Med_2s_avg
A         33         12         34         80         71         24
B         12         12         14         90         89         36
C         44         24         24          0         28         62
D         43         23         34         10         14         22
E         67         32         44         12         21         85
F         12         62         54         20         31         45
G         88         72         64         30         45         63
H         23         82         74         40         62         12
I         11         92         84         50         61          2
```

If the csv files name are not correct or the datasets in csv are less than three row, it will return Error.


## generate all user's summary result into one file

Sort out the data of each english letter group corresponding to all testers, expected result: 


(N means A-I)

```

summary_{N}.csv

        Att_0s_avg,Att_1s_avg,Att_2s_avg,Med_0s_avg,Med_1s_avg,Med_2s_avg
user1
user2
user2
...
```
