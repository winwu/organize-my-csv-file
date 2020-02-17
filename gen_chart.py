#!/usr/bin/python3

import os
import sys
import pathlib
from tabulate import tabulate

import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

from helpers.helpers import get_total_user_val
from helpers.log_colors import log_colors
from helpers.gconfig import gconfig
from helpers.initial import create_image_folders

dirname = os.path.dirname(__file__)

# total number of testers, default 0
# total_test_user = 0

att_df_for_csv_list = list()
med_df_for_csv_list = list()

def gen_all_avg_chart_by_category_of_each_user():
    for alphabet in gconfig.english_category_range:

        the_csv = './dist/by_alphabet/category_' + alphabet + '.csv'
        
        if not os.path.exists(the_csv):
            print('{}[Warning] {} not exists{}'.format(log_colors.WARNING, the_csv, log_colors.ENDC))
            return

        df = pd.read_csv(the_csv)
        
        # 所有類別的第一次到第三次實驗平均
        a_0_avg_123 = df.att_0s_avg_123.mean()
        a_1_avg_123 = df.att_1s_avg_123.mean()
        a_2_avg_123 = df.att_2s_avg_123.mean()
        m_0_avg_123 = df.med_0s_avg_123.mean()
        m_1_avg_123 = df.med_1s_avg_123.mean()
        m_2_avg_123 = df.med_2s_avg_123.mean()

        att_df = pd.DataFrame(columns = ['seconds', 'attention_average'])
        att_df.loc[0] = [0, a_0_avg_123]
        att_df.loc[1] = [1, a_1_avg_123]
        att_df.loc[2] = [2, a_2_avg_123]

        att_df_for_csv = pd.DataFrame(columns = ['0s', '1s', '2s'])
        att_df_for_csv.loc[alphabet] = [a_0_avg_123, a_1_avg_123, a_2_avg_123]
        att_df_for_csv_list.append(att_df_for_csv)

        med_df = pd.DataFrame(columns = ['seconds', 'meditation_average'])
        med_df.loc[0] = [0, m_0_avg_123]
        med_df.loc[1] = [1, m_1_avg_123]
        med_df.loc[2] = [2, m_2_avg_123]

        med_df_for_csv = pd.DataFrame(columns = ['0s', '1s', '2s'])
        med_df_for_csv.loc[alphabet] = [m_0_avg_123, m_1_avg_123, m_2_avg_123]
        med_df_for_csv_list.append(med_df_for_csv)
        
        # attention
        print(
            '--------',
            'category: {} : the attention average of 3 times data of all users'.format(alphabet),
            tabulate(att_df, headers = 'keys', tablefmt = 'psql'),
            sep="\n")
        fig = px.line(att_df, x = 'seconds', y = 'attention_average', title = 'Average Result of all test of type: ' + alphabet)
        fig.update_layout(
            xaxis = dict(
                dtick = 1
            )
        )
        fig.write_image('./dist/images/avg_123/attention/category_' + alphabet + '_123.png', width = 700, scale = 2)


        # meditation
        print(
            '--------',
            'category: {} : the meditation average of 3 times data of all users'.format(alphabet),
            tabulate(med_df, headers = 'keys', tablefmt = 'psql'),
            sep="\n")
        fig2 = px.line(med_df, x = 'seconds', y = 'meditation_average', title = 'Average Result of all test of type: ' + alphabet)
        fig2.update_layout(
            xaxis = dict(
                dtick = 1
            )
        )
        fig2.write_image('./dist/images/avg_123/meditation/category_' + alphabet + '_123.png', width = 700, scale = 2)
            
        #fig.show()

def gen_all_user_of_3_times_avg_csv():
    
    path = './dist/images/avg_123'
    
    print('att_df_for_csv_list')
    att_avg_df = pd.concat(att_df_for_csv_list)
    att_avg_df.index.name = 'category'
    att_avg_df.to_csv(path + 'attention_avg_123.csv', encoding = 'utf-8', index = True)
    
    # orient:
    # index => object's key name by category
    # columns => object's key name by 0s, 1s, 2s
    # att_avg_df.to_json(os.path.join(dirname, path + 'attention_avg_123.json'), orient = 'index')
    print(tabulate(att_avg_df, headers = 'keys', tablefmt = 'psql'))
    
    # 製作 line chart
    att_avg_df.T.plot()
    plt.title('All user each second average attention')
    plt.savefig(path + 'attention_avg_123.png')

    
    print('med_df_for_csv_list')
    med_avg_df = pd.concat(med_df_for_csv_list)
    med_avg_df.index.name = 'category'
    med_avg_df.to_csv(path + 'meditation_avg_123.csv', encoding = 'utf-8', index = True)
    # med_avg_df.to_json(os.path.join(dirname, path + 'meditation_avg_123.json'), orient = 'index')
    print(tabulate(med_avg_df, headers = 'keys', tablefmt = 'psql'))
    
    # 製作 line chart
    med_avg_df.T.plot()
    plt.title('All user each second average meditation')
    plt.savefig(path + 'meditation_avg_123.png')


if __name__ == "__main__":
    # total_test_user = int(get_total_user_val(sys.argv[1:]))
    create_image_folders()
    
    # 產生每個類別所有使用者三次三秒平均數值
    gen_all_avg_chart_by_category_of_each_user()
    
    # 產生所有類別三次平均數值的 csv
    gen_all_user_of_3_times_avg_csv()
    
    