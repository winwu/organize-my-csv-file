#!/usr/bin/python3

import os
import sys

from tabulate import tabulate
import pandas as pd

from helpers.helpers import get_total_user_val
from helpers.helpers import is_validate_csv_filename
from helpers.log_colors import log_colors
from helpers.gconfig import gconfig
from helpers.initial import create_folders

dirname = os.path.dirname(__file__)

# 測試者總數, 預設 0
total_test_user = 0

# 定義所要產生的欄位
col_names = [
    # 計算第一次, 第二次以及第三次的 0~2 秒的平均值
    'att_0s_avg_123',  # 預期結果: (第一次 Attention 0s + 第二次  Attention 0s + 第三次 Attention 0s)/3
    'att_1s_avg_123',  # 預期結果: (第一次 Attention 1s + 第二次  Attention 1s + 第三次 Attention 1s)/3
    'att_2s_avg_123',  # 預期結果: (第一次 Attention 2s + 第二次  Attention 2s + 第三次 Attention 2s)/3
    'med_0s_avg_123',  # 預期結果: (第一次 Meditation 0s + 第二次  Meditation 0s + 第三次 Meditation 0s)/3
    'med_1s_avg_123',  # 預期結果: (第一次 Meditation 1s + 第二次  Meditation 1s + 第三次 Meditation 1s)/3
    'med_2s_avg_123',  # 預期結果: (第一次 Meditation 2s + 第二次  Meditation 2s + 第三次 Meditation 2s)/3
    
    # 只計算第二次與第三次的平均值
    'att_0s_avg_23',   # 預期結果: (第二次  Attention 0s + 第三次 Attention 0s)/2
    'att_1s_avg_23',   # 預期結果: (第二次  Attention 1s + 第三次 Attention 1s)/2
    'att_2s_avg_23',   # 預期結果: (第二次  Attention 2s + 第三次 Attention 2s)/2
    'med_0s_avg_23',   # 預期結果: (第二次  Meditation 0s + 第三次 Meditation 0s)/2
    'med_1s_avg_23',   # 預期結果: (第二次  Meditation 1s + 第三次 Meditation 1s)/2
    'med_2s_avg_23'    # 預期結果: (第二次  Meditation 2s + 第三次 Meditation 2s)/2
]

def generate_result_by_user():
    for user_id in range(1, total_test_user + 1):
        
        # 1. 搜尋 ds 底下符合規則的資料夾
        user_path = os.path.join(dirname, 'data_source/tester' + str(user_id))
        
        if not os.path.exists(user_path):
            print('{}[Warning]\n Tester: {}\'s data source not exists.{}'.format(log_colors.WARNING, user_id, log_colors.ENDC))
        else: 
            # 2. 為每個 user 建立 user_sum_df 以利計算結果放到這張表
            user_sum_df = pd.DataFrame(index = list(gconfig.english_type_range), columns = col_names)
            user_sum_df.index.name = 'type'
            
            # set all cell value to -999 as default
            user_sum_df.fillna(-999, inplace = True)
            print('{}[Processing] folder: {}{}'.format(log_colors.BLUE, user_id, log_colors.ENDC))
        
            # 3. categories file names according to English alphabet (A~I)
            for alphabet in gconfig.english_type_range:
                
                each_eng_type_list = []
                
                for csv_fname in os.listdir(user_path):
                    if is_validate_csv_filename(alphabet, csv_fname):
                        each_eng_type_list.append(csv_fname)
                    
                # update file sequance from 1 -> 2 -> 3
                each_eng_type_list = sorted(each_eng_type_list)

                print('-Type: {}\'s List: {}-'.format(alphabet, each_eng_type_list))

                # all groups must have three files to be continue...
                is_all_csv_ready = len(each_eng_type_list) == 3

                if is_all_csv_ready:
                    print(' Start generating csv for this type {}...'.format(alphabet))
                    
                    tmpPdList = list()
                    # concat csv into one
                    for csv in each_eng_type_list:
                        csvPath = './data_source/tester' + str(user_id) + '/' + csv
                        # print('CSV path: {}'.format(csvPath))
                        tmpDf = pd.read_csv(csvPath, nrows = 3, usecols = ['Attention', 'Meditation'])
                        #print(tmpDf)
                        tmpPdList.append(tmpDf)

                    # 把每個英文字母的分別三次的每秒數值合成一張暫時的表 current_alphabet_df
                    #       Attention  Meditation
                    # 0         47          60
                    # 1         53          69
                    # 2         53          61
                    # 0         56          56
                    # 1         69          60
                    # 2         81          60
                    # 0         69          67
                    # 1         63          57
                    # 2         54          43
                    current_alphabet_df = pd.concat(tmpPdList)
                    
                    print(tabulate(current_alphabet_df, headers='keys', tablefmt='psql'))
                    
                    # print('測是 Attention 1_0 ', current_alphabet_df['Attention'].values[0])

                    # print('測是 Attention 2_1 ', current_alphabet_df['Attention'].values[3])

                    # print('測是 Attention 3_1 ', current_alphabet_df['Attention'].values[6])
                    
                    # 計算三次實驗的每一秒平均值，例如 (第一次 0s +第二次 0s + 第三次 0s)/3... 以此類推
                    user_sum_df.at[alphabet, 'att_0s_avg_123'] = round(current_alphabet_df.at[0, 'Attention'].mean(), 3) if len(current_alphabet_df.at[0, 'Attention']) == 3 else -999	
                    user_sum_df.at[alphabet, 'att_1s_avg_123'] = round(current_alphabet_df.at[1, 'Attention'].mean(), 3) if len(current_alphabet_df.at[1, 'Attention']) == 3 else -999
                    user_sum_df.at[alphabet, 'att_2s_avg_123'] = round(current_alphabet_df.at[2, 'Attention'].mean(), 3) if len(current_alphabet_df.at[2, 'Attention']) == 3 else -999
                    user_sum_df.at[alphabet, 'med_0s_avg_123'] = round(current_alphabet_df.at[0, 'Meditation'].mean(), 3) if len(current_alphabet_df.at[0, 'Meditation']) == 3 else -999
                    user_sum_df.at[alphabet, 'med_1s_avg_123'] = round(current_alphabet_df.at[1, 'Meditation'].mean(), 3) if len(current_alphabet_df.at[1, 'Meditation']) == 3 else -999
                    user_sum_df.at[alphabet, 'med_2s_avg_123'] = round(current_alphabet_df.at[2, 'Meditation'].mean(), 3) if len(current_alphabet_df.at[2, 'Meditation']) == 3 else -999
                    
                    # 計算第二次跟第三次實驗的每一秒平均值，例如 att_0s_avg_23 = (第二次 attention 的 0s + 第三次 attention 的 0s)/2... 以此類推
                    user_sum_df.at[alphabet, 'att_0s_avg_23'] = round((current_alphabet_df['Attention'].values[3] + current_alphabet_df['Attention'].values[6]) / 2)
                    user_sum_df.at[alphabet, 'att_1s_avg_23'] = round((current_alphabet_df['Attention'].values[4] + current_alphabet_df['Attention'].values[7]) / 2)
                    user_sum_df.at[alphabet, 'att_2s_avg_23'] = round((current_alphabet_df['Attention'].values[5] + current_alphabet_df['Attention'].values[8]) / 2)
                    user_sum_df.at[alphabet, 'med_0s_avg_23'] = round((current_alphabet_df['Meditation'].values[3] + current_alphabet_df['Meditation'].values[6]) / 2)
                    user_sum_df.at[alphabet, 'med_1s_avg_23'] = round((current_alphabet_df['Meditation'].values[4] + current_alphabet_df['Meditation'].values[4]) / 2)
                    user_sum_df.at[alphabet, 'med_2s_avg_23'] = round((current_alphabet_df['Meditation'].values[5] + current_alphabet_df['Meditation'].values[8]) / 2)

            print(tabulate(user_sum_df, headers='keys', tablefmt='psql'))
            user_sum_df.to_csv(os.path.join(dirname, 'dist/by_tester/tester' + str(user_id) + '.csv'), encoding = 'utf-8', index = True)

def generate_result_by_alphabet():
    print('------ 依照英文字母整理資料 ------')
    missing_tester_list = list()
    
    for alphabet in gconfig.english_type_range:
        alphabet_df = pd.DataFrame(index = list(range(1, total_test_user + 1)), columns = col_names)
        alphabet_df.index.name = 'tester'
        alphabet_df.fillna(-2, inplace = True)
        
        print('------------------------- alphabet: {} -----------------------------'.format(alphabet))

        for i in range(1, total_test_user + 1):
            # 讀取每位使用者的資料
            tester_sum_csv_path = os.path.join(dirname, 'dist/by_tester/tester' + str(i) + '.csv')
            
            if os.path.exists(tester_sum_csv_path):
                user_summary_df = pd.read_csv(tester_sum_csv_path)
                # 依照英文字母去讀去每 row
                
                row_data = user_summary_df.query('type == \'' + alphabet + '\'')
                
                if ((row_data.att_0s_avg_123 != -999).bool() 
                    and (row_data.att_1s_avg_123 != -999).bool()
                    and (row_data.att_2s_avg_123 != -999).bool()
                    and (row_data.med_0s_avg_123 != -999).bool()
                    and (row_data.med_1s_avg_123 != -999).bool()
                    and (row_data.med_2s_avg_123 != -999).bool()):
                    
                    for rowname in col_names:
                        alphabet_df.at[i, rowname] = row_data[rowname]       
            else:
                if tester_sum_csv_path not in missing_tester_list:
                    missing_tester_list.append(tester_sum_csv_path)
            
        # print('before droped')
        # print(tabulate(alphabet_df, headers = 'keys', tablefmt = 'psql'))
        
        #  移除沒有意義的 row. 例如數值包含一開始設定的 -2
        for rowname in col_names:
            alphabet_df.drop(alphabet_df.loc[alphabet_df[rowname] == -2].index, inplace = True)
        
        print('type_' +  alphabet + '.csv')
        print(tabulate(alphabet_df, headers = 'keys', tablefmt = 'psql'))
        
        alphabet_df.to_csv(os.path.join(dirname, 'dist/by_alphabet/type_' + alphabet + '.csv'), encoding = 'utf-8', index = True)
        
    if len(missing_tester_list) > 0:
        print('{}[Warning]\n {} Skiped due to data_source not exists or format not correct.{}'
            .format(log_colors.WARNING, ',\n'.join(missing_tester_list), log_colors.ENDC))


def generate_alphabet_describe():
    for alphabet in gconfig.english_type_range:
        # 讀取每位使用者的資料
        alphabet_csv = os.path.join(dirname, 'dist/by_alphabet/type_' + str(alphabet) + '.csv')
        
        if os.path.exists(alphabet_csv):
            this_df = pd.read_csv(alphabet_csv).describe()
            this_df = this_df.drop('tester', 1)
            
            # 描述統計
            print(' ----------------- 形式 {} 的敘述統計 -----------------'.format(alphabet))
            print(this_df)
            this_df.to_csv(os.path.join(dirname, 'dist/by_alphabet_describe/' + alphabet + '.csv'), encoding = 'utf-8', index = True)
            # print('att_0s_avg_123 平均值: {}'.format(this_df['att_0s_avg_123'].mean()))


if __name__ == "__main__":
   total_test_user = int(get_total_user_val(sys.argv[1:]))
   create_folders()
   generate_result_by_user()
   generate_result_by_alphabet()
   generate_alphabet_describe()