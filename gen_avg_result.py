#!/usr/bin/python3

import os
import sys
import pathlib
from tabulate import tabulate

from plotly.offline import iplot
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

from helpers.helpers import get_total_user_val
from helpers.log_colors import log_colors
from helpers.gconfig import gconfig

dirname = os.path.dirname(__file__)

# total number of testers, default 0
# total_test_user = 0

att_df_for_csv_list = list()
med_df_for_csv_list = list()

def initial():
    if not os.path.exists(os.path.join(dirname, 'dist/images')):
        pathlib.Path(os.path.join(dirname, 'dist/images')).mkdir(parents = True, exist_ok = True)

    if not os.path.exists(os.path.join(dirname, 'dist/images/all_times_avg')):
        pathlib.Path(os.path.join(dirname, 'dist/images/all_times_avg')).mkdir(parents = True, exist_ok = True)
    
    if not os.path.exists(os.path.join(dirname, 'dist/images/all_times_avg/attention')):
        pathlib.Path(os.path.join(dirname, 'dist/images/all_times_avg/attention')).mkdir(parents = True, exist_ok = True)
    
    if not os.path.exists(os.path.join(dirname, 'dist/images/all_times_avg/meditation')):
        pathlib.Path(os.path.join(dirname, 'dist/images/all_times_avg/meditation')).mkdir(parents = True, exist_ok = True)

def gen_all_avg_chart_by_category_of_each_user():
    for alphabet in gconfig.english_category_range:

        the_csv = './dist/by_alphabet/category_' + alphabet + '.csv'
        
        if not os.path.exists(the_csv):
            print('{}[Warning] {} not exists{}'.format(log_colors.WARNING, the_csv, log_colors.ENDC))
            return

        df = pd.read_csv(the_csv)
        
        # print(df)

        a_0_avg = df.Attention_0s_avg.mean()
        a_1_avg = df.Attention_1s_avg.mean()
        a_2_avg = df.Attention_2s_avg.mean()

        m_0_avg = df.Meditation_0s_avg.mean()
        m_1_avg = df.Meditation_1s_avg.mean()
        m_2_avg = df.Meditation_2s_avg.mean()

        # table = ff.create_table(df)
        # iplot(table, filename='jupyter-table1')

        att_df = pd.DataFrame(columns = ['seconds', 'attention_average'])
        att_df.loc[0] = [0, a_0_avg]
        att_df.loc[1] = [1, a_1_avg]
        att_df.loc[2] = [2, a_2_avg]

        att_df_for_csv = pd.DataFrame(columns = ['0s', '1s', '2s'])
        att_df_for_csv.loc[alphabet] = [a_0_avg, a_1_avg, a_2_avg]
        att_df_for_csv_list.append(att_df_for_csv)

        med_df = pd.DataFrame(columns = ['seconds', 'meditation_average'])
        med_df.loc[0] = [0, m_0_avg]
        med_df.loc[1] = [1, m_1_avg]
        med_df.loc[2] = [2, m_2_avg]

        med_df_for_csv = pd.DataFrame(columns = ['0s', '1s', '2s'])
        med_df_for_csv.loc[alphabet] = [m_0_avg, m_1_avg, m_2_avg]
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
        fig.write_image('./dist/images/all_times_avg/attention/all_user_3_times_avg_category_' + alphabet + '.png', width = 700, scale = 2)


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
        fig2.write_image('./dist/images/all_times_avg/meditation/all_user_3_times_avg_category_' + alphabet + '.png', width = 700, scale = 2)
            
        #fig.show()

def gen_all_user_of_3_times_avg_csv():
    
    print('att_df_for_csv_list')
    att_avg_df = pd.concat(att_df_for_csv_list)
    att_avg_df.index.name = 'category'
    att_avg_df.to_csv('./dist/by_alphabet/all_times_avg_attention.csv', encoding = 'utf-8', index = True)
    # orient:
    # index => object's key name by category
    # columns => object's key name by 0s, 1s, 2s
    att_avg_df.to_json(os.path.join(dirname, 'dist/by_alphabet/all_user_3_times_attention_avg.json'), orient = 'index')
    print(tabulate(att_avg_df, headers = 'keys', tablefmt = 'psql'))
    
    
    print('med_df_for_csv_list')
    med_avg_df = pd.concat(med_df_for_csv_list)
    med_avg_df.index.name = 'category'
    med_avg_df.to_csv('./dist/by_alphabet/all_times_avg_meditation.csv', encoding = 'utf-8', index = True)
    med_avg_df.to_json(os.path.join(dirname, 'dist/by_alphabet/all_user_3_times_meditation_avg.json'), orient = 'index')
    print(tabulate(med_avg_df, headers = 'keys', tablefmt = 'psql'))


if __name__ == "__main__":
    # total_test_user = int(get_total_user_val(sys.argv[1:]))
    initial()
    
    # 產生每個類別所有使用者三次三秒平均數值
    gen_all_avg_chart_by_category_of_each_user()
    
    # 產生所有類別三次平均數值的 csv
    gen_all_user_of_3_times_avg_csv()
    
    