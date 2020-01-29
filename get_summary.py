#!/usr/bin/python3

import os
import sys
import string
import re
from tabulate import tabulate
import pandas as pd

from helpers.helpers import get_total_user_val 
from helpers.log_colors import log_colors

# all variables

# categories are named by English alphabet from A to I
english_category_range = string.ascii_uppercase[:9]

# total number of testers, default 0
total_test_user = 0

# define new columns which we need
col_names = [
    'Att_0s_avg', # Average attention value of the 0th second of all data
    'Att_1s_avg', # Average attention value of the 1st second of all data
    'Att_2s_avg', # Average attention value of the 2nd second of all data
    'Med_0s_avg', # Meditation attention value of the 0th second of all data
    'Med_1s_avg', # Meditation attention value of the 1st second of all data
    "Med_2s_avg"  # Meditation attention value of the 2nd second of all data
]

useful_field_we_needs = ['Attention', 'Meditation']

dist_path = './dist'

def initial():
    # step1: make sure data_source exists
    if not os.path.exists('./data_source'):
        os.makedirs('./data_source')
    
    # step2. create by_tester folder under ./dist
    if not os.path.exists(dist_path + '/by_tester'):
        os.makedirs(dist_path + '/by_tester')
    
    # step3. create by_alphabet folder under ./dist
    if not os.path.exists(dist_path + '/by_alphabet'):
        os.makedirs(dist_path + '/by_alphabet')

# TODO check if file name valid

def generate_summary_by_user():
    for user_id in range(1, total_test_user + 1):
        # search for all tester{N} folder in data_source
        user_path = './data_source/tester' + str(user_id)
        
        if not os.path.exists(user_path):
            print('{}[Warning] Tester: {}\'s data source not exists.{}'.format(log_colors.WARNING, user_id, log_colors.ENDC))
        else: 
            # 2. init summary table df of each user
            user_sum_df = pd.DataFrame(index = list(english_category_range), columns = col_names)
            user_sum_df.index.name = 'category'
            # set all cell value to -999 as default
            user_sum_df.fillna(-999, inplace = True)
            print('{}[Processing] folder: {}{}'.format(log_colors.BLUE, user_id, log_colors.ENDC))
        
            # 3. categories file names according to English alphabet (A~I)
            for alphabet in english_category_range:
                
                each_eng_category_list = []
                
                for csv_fname in os.listdir(user_path):
                    # search pattern like: 1-A-1.csv ~ 1-A-3.csv
                    if re.match("(^[1-9]-[" + re.escape(alphabet) + "]-[1-3]).csv", csv_fname):
                        each_eng_category_list.append(csv_fname)
                    
                # update file sequance from 1 -> 2 -> 3
                each_eng_category_list = sorted(each_eng_category_list)

                print('Category: {}\'s List: {}'.format(alphabet, each_eng_category_list))

                # all groups must have three files to be continue...
                is_all_csv_ready = len(each_eng_category_list) == 3

                if is_all_csv_ready:
                    print('Start to generate summary csv for this category...')
                    
                    tmpPdList = list()
                    # concat csv into one
                    for csv in each_eng_category_list:
                        csvPath = './data_source/tester' + str(user_id) + '/' + csv
                        # print('CSV path: {}'.format(csvPath))
                        tmpDf = pd.read_csv(csvPath, nrows = 3, usecols = useful_field_we_needs)
                        #print(tmpDf)
                        tmpPdList.append(tmpDf)

                    result_df = pd.concat(tmpPdList)

                    # group 3 df's value by 0, 1, 2 and calculate the average for each seconds average
                    # length mush be 3 with each average lists

                    user_sum_df.at[alphabet, 'Att_0s_avg'] = round(result_df.at[0, 'Attention'].mean(), 3) if len(result_df.at[2, 'Attention']) == 3 else -999
                    user_sum_df.at[alphabet, 'Att_1s_avg'] = round(result_df.at[1, 'Attention'].mean(), 3) if len(result_df.at[1, 'Attention']) == 3 else -999
                    user_sum_df.at[alphabet, 'Att_2s_avg'] = round(result_df.at[2, 'Attention'].mean(), 3) if len(result_df.at[2, 'Attention']) == 3 else -999
                    user_sum_df.at[alphabet, 'Med_0s_avg'] = round(result_df.at[0, 'Meditation'].mean(), 3) if len(result_df.at[0, 'Meditation']) == 3 else -999
                    user_sum_df.at[alphabet, 'Med_1s_avg'] = round(result_df.at[1, 'Meditation'].mean(), 3) if len(result_df.at[1, 'Meditation']) == 3 else -999
                    user_sum_df.at[alphabet, 'Med_2s_avg'] = round(result_df.at[2, 'Meditation'].mean(), 3) if len(result_df.at[2, 'Meditation']) == 3 else -999

            print(tabulate(user_sum_df, headers='keys', tablefmt='psql'))

            user_sum_df.to_csv(dist_path + '/by_tester/tester' + str(user_id) + '.csv', encoding = 'utf-8', index = True)

def generate_summary_by_alphabet():
    print('------ generate_summary_by_alphabet ------')
    missing_tester_list = list()
    
    for alphabet in english_category_range:
        alphabet_df = pd.DataFrame(index = list(range(1, total_test_user + 1)), columns = col_names)
        alphabet_df.index.name = 'tester'
        alphabet_df.fillna(-2, inplace = True)
        
        print('------------------------- alphabet: {} -----------------------------'.format(alphabet))

        for i in range(1, total_test_user + 1):
            # read file summary/tester1~total_test_user.csv
            tester_sum_csv_path = dist_path + '/by_tester/tester' + str(i) + '.csv'
            
            if os.path.exists(tester_sum_csv_path):
                user_summary_df = pd.read_csv(dist_path + '/by_tester/tester' + str(i) + '.csv')
                # pick sepecific row by alphabet
                row_data = user_summary_df.query('category == \'' + alphabet + '\'')
                
                if ((row_data.Att_0s_avg != -999).bool() and (row_data.Att_1s_avg != -999).bool() and (row_data.Att_2s_avg != -999).bool() and (row_data.Med_0s_avg != -999).bool() and (row_data.Med_1s_avg != -999).bool() and (row_data.Med_2s_avg != -999).bool()):
                    alphabet_df.at[i, 'Att_0s_avg'] = row_data.Att_0s_avg
                    alphabet_df.at[i, 'Att_1s_avg'] = row_data.Att_1s_avg
                    alphabet_df.at[i, 'Att_2s_avg'] = row_data.Att_2s_avg
                    alphabet_df.at[i, 'Med_0s_avg'] = row_data.Med_0s_avg
                    alphabet_df.at[i, 'Med_1s_avg'] = row_data.Med_1s_avg
                    alphabet_df.at[i, 'Med_2s_avg'] = row_data.Med_2s_avg
            else:
                if tester_sum_csv_path not in missing_tester_list:
                    missing_tester_list.append(tester_sum_csv_path)
            
    
        
        # drop no-used row
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Att_0s_avg'] == -2].index, inplace = True)
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Att_1s_avg'] == -2].index, inplace = True)
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Att_2s_avg'] == -2].index, inplace = True)
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Med_0s_avg'] == -2].index, inplace = True)
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Med_1s_avg'] == -2].index, inplace = True)
        alphabet_df.drop(alphabet_df.loc[alphabet_df['Med_2s_avg'] == -2].index, inplace = True)
        
        print('category_' +  alphabet + '.csv')
        print(tabulate(alphabet_df, headers='keys', tablefmt='psql'))
        
        alphabet_df.to_csv(dist_path + '/by_alphabet' + '/category_' +  alphabet + '.csv', encoding = 'utf-8', index = True)

    if len(missing_tester_list) > 0:
        print('{}[Warning] {} Skiped due to data_source not exists or format not correct.{}'
            .format(log_colors.WARNING, ',\n'.join(missing_tester_list), log_colors.ENDC))


if __name__ == "__main__":
   total_test_user = int(get_total_user_val(sys.argv[1:]))
   initial()
   generate_summary_by_user()
   generate_summary_by_alphabet()