#!/usr/bin/python3
import os
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from helpers.log_colors import log_colors

def gen_chart():
    gen_list = [
        'attention_avg_123',
        'attention_avg_23',
        'meditation_avg_123',
        'meditation_avg_23'
    ]

    for csv_name in gen_list:
        print(csv_name)
        
        csv_path = os.path.join('./dist/' + str(csv_name) + '.csv')
        print(csv_path)
        
        if not os.path.exists(csv_path):
            print('{}[Warning]\n: {}\'not exists.{}'.format(log_colors.WARNING, csv_path, log_colors.ENDC))
        else:
            df = pd.read_csv(csv_path, index_col = 0)
            print('----------- {} -------------\n'.format(str(csv_path)))
            print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
            
            df.T.plot(figsize=(10,5))
            plt.title(csv_name)
            plt.savefig('./dist/' + csv_name + '.png', format="png",  dpi = 200)


if __name__ == "__main__":
    gen_chart()