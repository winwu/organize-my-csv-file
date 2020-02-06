# The analysis of experimental data results of my lab

The purpose of this repo is to organize the eeg data and convert it to the format I need.

It's require Python 3, Pandas, plotly...etc, to install these packages:



```
pip3 install pandas
pip3 install plotly==4.5.0
pip3 install tabulate
npm install -g electron@1.8.4 orca
pip3 install psutil requests
```

for Mac user:

```
python3 -m pip uninstall pip
pip3 install pandas --user
pip3 install plotly==4.5.0 --user
pip3 install tabulate --user
npm install -g electron@1.8.4 orca
pip3 install psutil requests
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
├── tester2
├── ├── ...
```

* each csv file name are correct format: `[1-9]-[A-I]-[1-3]).csv`.
* after all files in data_source prepare well, run:

```Shell
python3 get_summary.py -i <total_user_count>
```

or

```Shell
./get_summary.py -i <total_user_count>
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


## Generate all average result by category

```Shell
python3 gen_avg_result.py -i <total_user_count>
```

or

```Shell
./gen_avg_result.py -i <total_user_count>
```

The example result:

```
att_df_for_csv_list
+------------+---------+---------+---------+
| category   |      0s |      1s |      2s |
|------------+---------+---------+---------|
| A          | xxx     |xxx      |xxx      |
| B          | xxx     |xxx      |xxx      |
| C          | xxx     |xxx      |xxx      |
| ...        | xxx     |xxx      |xxx      |
+------------+---------+---------+---------+
med_df_for_csv_list
+------------+---------+---------+---------+
| category   |      0s |      1s |      2s |
|------------+---------+---------+---------|
| A          | xxx     |xxx      |xxx      |
| B          | xxx     |xxx      |xxx      |
| C          | xxx     |xxx      |xxx      |
| ...        | xxx     |xxx      |xxx      |
+------------+---------+---------+---------
```


# Online resources

* https://nbviewer.jupyter.org/github/pybokeh/jupyter_notebooks/blob/master/plotly/plotly_with_pandas.html