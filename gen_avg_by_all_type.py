#!/usr/bin/python3

import os
from tabulate import tabulate

import pandas as pd
# import matplotlib.pyplot as plt

from helpers.log_colors import log_colors
from helpers.gconfig import gconfig
# from helpers.initial import create_image_folders

def gen_avg_by_all():
    # 總共有四張新表
    columns = ['0s', '1s', '2s']
    
    att_df_123 = pd.DataFrame(index = list(gconfig.english_type_range), columns = columns)
    att_df_123.index.name = 'type'
    
    att_df_23 = pd.DataFrame(index = list(gconfig.english_type_range), columns = columns)
    att_df_23.index.name = 'type'

    med_df_123 = pd.DataFrame(index = list(gconfig.english_type_range), columns = columns)
    med_df_123.index.name = 'type'
    
    med_df_23 = pd.DataFrame(index = list(gconfig.english_type_range), columns = columns)
    med_df_23.index.name = 'type'

    for alphabet in gconfig.english_type_range:

        the_csv = './dist/by_alphabet/type_' + alphabet + '.csv'
        
        if not os.path.exists(the_csv):
            print('{}[Warning] {} not exists{}'.format(log_colors.WARNING, the_csv, log_colors.ENDC))
            return

        df = pd.read_csv(the_csv)
        # 所有類別的第一次到第三次實驗平均
        
        # 處理 attention
        a_0_avg_123 = df.att_0s_avg_123.mean()
        a_1_avg_123 = df.att_1s_avg_123.mean()
        a_2_avg_123 = df.att_2s_avg_123.mean()

        a_0_avg_23 = df.att_0s_avg_23.mean()
        a_1_avg_23 = df.att_1s_avg_23.mean()
        a_2_avg_23 = df.att_2s_avg_23.mean()
        
        att_df_123.loc[alphabet] = [a_0_avg_123, a_1_avg_123, a_2_avg_123]
        att_df_23.loc[alphabet] = [a_0_avg_23, a_1_avg_23, a_2_avg_23]
        
        # 處理 meditation
        m_0_avg_123 = df.med_0s_avg_123.mean()
        m_1_avg_123 = df.med_1s_avg_123.mean()
        m_2_avg_123 = df.med_2s_avg_123.mean()
        
        m_0_avg_23 = df.med_0s_avg_23.mean()
        m_1_avg_23 = df.med_1s_avg_23.mean()
        m_2_avg_23 = df.med_2s_avg_23.mean()
        
        med_df_123.loc[alphabet] = [m_0_avg_123, m_1_avg_123, m_2_avg_123]
        med_df_23.loc[alphabet] = [m_0_avg_23, m_1_avg_23, m_2_avg_23]
        
    
    print('------ Attention 三次平均結果: ------\n{}\n'.format(tabulate(att_df_123, headers = 'keys', tablefmt = 'psql')))
    print('------ Meditation 三次平均結果: ------ \n{}\n'.format(tabulate(med_df_123, headers = 'keys', tablefmt = 'psql')))
    print('------ Attention 最後兩次平均結果: ------\n{}\n'.format(tabulate(att_df_23, headers = 'keys', tablefmt = 'psql')))
    print('------ Meditation 最後兩次平均結果: ------ \n{}\n'.format(tabulate(med_df_23, headers = 'keys', tablefmt = 'psql')))
    
    path = './dist/'

    att_df_123.to_csv(path + 'attention_avg_123.csv', encoding = 'utf-8', index = True)
    att_df_23.to_csv(path + 'attention_avg_23.csv', encoding = 'utf-8', index = True)
    med_df_123.to_csv(path + 'meditation_avg_123.csv', encoding = 'utf-8', index = True)
    med_df_23.to_csv(path + 'meditation_avg_23.csv', encoding = 'utf-8', index = True)

if __name__ == "__main__":
    # create_image_folders()
    # 產生所有類別的所有使用者三次三秒以及第二次第三次的三秒平均數值
    
    gen_avg_by_all()