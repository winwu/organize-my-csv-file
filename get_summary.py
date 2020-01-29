#!/usr/bin/python3

import os
import sys
import pathlib
from tabulate import tabulate
import pandas as pd

from helpers.helpers import get_total_user_val
from helpers.helpers import is_validate_csv_filename
from helpers.log_colors import log_colors
from helpers.gconfig import gconfig

# all variables
dirname = os.path.dirname(__file__)

# total number of testers, default 0
total_test_user = 0

# define new columns which we need
col_names = [
    'Attention_0s_avg', # Average attention value of the 0th second of all data
    'Attention_1s_avg', # Average attention value of the 1st second of all data
    'Attention_2s_avg', # Average attention value of the 2nd second of all data
    'Meditation_0s_avg', # Meditation attention value of the 0th second of all data
    'Meditation_1s_avg', # Meditation attention value of the 1st second of all data
    "Meditation_2s_avg"  # Meditation attention value of the 2nd second of all data
]

useful_field_we_needs = ['Attention', 'Meditation']

def initial():
    # create folder if not exists
    if not os.path.exists(os.path.join(dirname, 'data_source')):
        os.makedirs(os.path.join(dirname, 'data_source'))

    if not os.path.exists(os.path.join(dirname, 'dist/by_tester')):
        pathlib.Path(os.path.join(dirname, 'dist/by_tester')).mkdir(parents = True, exist_ok = True) 
    
    if not os.path.exists(os.path.join(dirname, 'dist/by_alphabet')):
        pathlib.Path(os.path.join(dirname, 'dist/by_alphabet')).mkdir(parents = True, exist_ok = True) 

# TODO check if file name valid

def generate_summary_by_user():
    for user_id in range(1, total_test_user + 1):
        # search for all tester{N} folder in data_source
        user_path = os.path.join(dirname, 'data_source/tester' + str(user_id))
        
        if not os.path.exists(user_path):
            print('{}[Warning] Tester: {}\'s data source not exists.{}'.format(log_colors.WARNING, user_id, log_colors.ENDC))
        else: 
            # 2. init summary table df of each user
            user_sum_df = pd.DataFrame(index = list(gconfig.english_category_range), columns = col_names)
            user_sum_df.index.name = 'category'
            # set all cell value to -999 as default
            user_sum_df.fillna(-999, inplace = True)
            print('{}[Processing] folder: {}{}'.format(log_colors.BLUE, user_id, log_colors.ENDC))
        
            # 3. categories file names according to English alphabet (A~I)
            for alphabet in gconfig.english_category_range:
                
                each_eng_category_list = []
                
                for csv_fname in os.listdir(user_path):
                    if is_validate_csv_filename(alphabet, csv_fname):
                        each_eng_category_list.append(csv_fname)
                    
                # update file sequance from 1 -> 2 -> 3
                each_eng_category_list = sorted(each_eng_category_list)

                print('-Category: {}\'s List: {}-'.format(alphabet, each_eng_category_list))

                # all groups must have three files to be continue...
                is_all_csv_ready = len(each_eng_category_list) == 3

                if is_all_csv_ready:
                    print(' Start generating csv for this category {}...'.format(alphabet))
                    
                    tmpPdList = list()
                    # concat csv into one
                    for csv in each_eng_category_list:
                        csvPath = './data_source/tester' + str(user_id) + '/' + csv
                        # print('CSV path: {}'.format(csvPath))
                        tmpDf = pd.read_csv(csvPath, nrows = 3, usecols = useful_field_we_needs)
                        #print(tmpDf)
                        tmpPdList.append(tmpDf)

                    # 把三次的結果合成一張暫時的表
                    # result_df looks like:
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
                    result_df = pd.concat(tmpPdList)
                    
                    # group 3 df's value by 0, 1, 2 and calculate the average for each seconds average
                    # length mush be 3 with each average lists
                    
                    for esense_type in useful_field_we_needs:
                        for test_sequence in range(0, 3):
                            # e.g. Attention_{X}s_avg, Meditation_{X}s_avg
                            store_col_name = esense_type + '_' + str(test_sequence) + 's_avg'
                            # print('store_col_name {}'.format(store_col_name))
                            # 會得到所有第 test_sequence 次的 esense_type 的值，e.g: [35 100 47]
                            the_test_seq_of_sense_vals = result_df.at[test_sequence, esense_type]
                            user_sum_df.at[alphabet, store_col_name] = round(the_test_seq_of_sense_vals.mean(), 3) if len(the_test_seq_of_sense_vals) == 3 else -999
            
            print(tabulate(user_sum_df, headers='keys', tablefmt='psql'))
            user_sum_df.to_csv(os.path.join(dirname, 'dist/by_tester/tester' + str(user_id) + '.csv'), encoding = 'utf-8', index = True)

def generate_summary_by_alphabet():
    print('------ generate_summary_by_alphabet ------')
    missing_tester_list = list()
    
    for alphabet in gconfig.english_category_range:
        alphabet_df = pd.DataFrame(index = list(range(1, total_test_user + 1)), columns = col_names)
        alphabet_df.index.name = 'tester'
        alphabet_df.fillna(-2, inplace = True)
        
        print('------------------------- alphabet: {} -----------------------------'.format(alphabet))

        for i in range(1, total_test_user + 1):
            # read file summary/tester1~total_test_user.csv
            tester_sum_csv_path = os.path.join(dirname, 'dist/by_tester/tester' + str(i) + '.csv')
            
            if os.path.exists(tester_sum_csv_path):
                user_summary_df = pd.read_csv(os.path.join(dirname, 'dist/by_tester/tester' + str(i) + '.csv'))
                # pick sepecific row by alphabet
                row_data = user_summary_df.query('category == \'' + alphabet + '\'')
                
                if ((row_data.Attention_0s_avg != -999).bool() 
                    and (row_data.Attention_1s_avg != -999).bool()
                    and (row_data.Attention_2s_avg != -999).bool()
                    and (row_data.Meditation_0s_avg != -999).bool()
                    and (row_data.Meditation_1s_avg != -999).bool()
                    and (row_data.Meditation_2s_avg != -999).bool()):
                    '''
                    0~2
                    alphabet_df.at[i, 'Attention_1s_avg'] = row_data.Attention_1s_avg
                    0~2
                    alphabet_df.at[i, 'Meditation_0s_avg'] = row_data.Meditation_0s_avg
                    '''
                    for esense_type in useful_field_we_needs:
                        for test_sequence in range(0, 3):
                            store_col_name = esense_type + '_' + str(test_sequence) + 's_avg'
                            alphabet_df.at[i, store_col_name] = row_data[store_col_name]
                    
            else:
                if tester_sum_csv_path not in missing_tester_list:
                    missing_tester_list.append(tester_sum_csv_path)
            
        
        # print('before droped')
        # print(tabulate(alphabet_df, headers = 'keys', tablefmt = 'psql'))
        
        
        # drop no-used row, such as some tester data_source are not exists or not well formated
        for esense_type in useful_field_we_needs:
            for test_sequence in range(0, 3):
                '''
                alphabet_df.drop(alphabet_df.loc[alphabet_df['Attention_1s_avg'] == -2].index, inplace = True)
                alphabet_df.drop(alphabet_df.loc[alphabet_df['Meditation_0s_avg'] == -2].index, inplace = True)
                '''
                store_col_name = esense_type + '_' + str(test_sequence) + 's_avg'
                alphabet_df.drop(alphabet_df.loc[alphabet_df[store_col_name] == -2].index, inplace = True)
        
        print('category_' +  alphabet + '.csv')
        print(tabulate(alphabet_df, headers = 'keys', tablefmt = 'psql'))
        
        alphabet_df.to_csv(os.path.join(dirname, 'dist/by_alphabet/category_' + alphabet + '.csv'), encoding = 'utf-8', index = True)
        
    if len(missing_tester_list) > 0:
        print('{}[Warning] {} Skiped due to data_source not exists or format not correct.{}'
            .format(log_colors.WARNING, ',\n'.join(missing_tester_list), log_colors.ENDC))


if __name__ == "__main__":
   total_test_user = int(get_total_user_val(sys.argv[1:]))
   initial()
   generate_summary_by_user()
   generate_summary_by_alphabet()