# Analysis of experimental data results

The purpose of this project is to organize the data and convert it to the format needed to facilitate analysis.

use Python 3 and Pandas, need to isntall these packages:

```
pip3 install pandas

```

for Mac user:

```
pip3 install pandas --user 
```

## generate summary result by each user

Calculate the average of three data sets for each English alphabet group, will create summary result csv in each ./data_source/tester{N}/summary/summary_tester{N}.csv

run `python3 combine_with_loop.py`


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

