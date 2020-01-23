#!/usr/bin/python3

# TODO: quantile

import os
import sys
import getopt
import string
import re
import pandas as pd

# all variables

# a list for all testers folder name
user_folders = list()

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

def main(argv):
    tmp_user_count = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["itotal_user_count="])
    except getopt.GetoptError:
        print ('combine_category_by_user.py -i <total_user_count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('combine_category_by_user.py -i <total_user_count>')
            sys.exit()
        elif opt in ("-i", "--itotal_user_count"):
            tmp_user_count = arg
            
    print('total user is: {}'.format(tmp_user_count))
    return tmp_user_count

def initial():
    # step1: make sure data_source exists
    if not os.path.exists('./data_source'):
        os.makedirs('./data_source')
    
    # step2: update user_folders array length tobe total_test_user value
    for i in range(1, total_test_user + 1):
        user_folders.append('tester' + str(i))

    # step3: create summary folder for each user
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

def generate_summary_csv():
    for tester_fname in user_folders:
        # 1. create folder for each test user if not exists
        if not os.path.exists('./data_source' + '/' + tester_fname):
            os.makedirs('./data_source' + '/' + tester_fname)

        # 2. create summary folder under ./dist
        sum_path = dist_path + '/summary'
        if not os.path.exists(sum_path):
            os.makedirs(sum_path)

        # 3. init summary table df of each user
        tester_summary_df = pd.DataFrame(index = list(english_category_range), columns = col_names)
        
        # set all cell value to 0 as default
        # tester_summary_df.fillna(0, inplace = True)

        print('---------- Processing folder: {} ----------'.format(tester_fname))

        # 4. categories file names according to English alphabet (A~I)
        for alphabet in english_category_range:
            
            tester_folder = './data_source' + '/' + tester_fname
            each_eng_category_list = []
            
            for name in os.listdir(tester_folder):
                # search pattern like: 1-A-1.csv ~ 1-A-3.csv
                if re.match("(^[1-9]-[" + re.escape(alphabet) + "]-[1-3]).csv", name):
                    each_eng_category_list.append(name)

            # update file sequance from 1 -> 2 -> 3
            each_eng_category_list = sorted(each_eng_category_list)

            print('Category {} List: {}'.format(alphabet, each_eng_category_list))

            # all groups must have three files to be continue...
            is_all_csv_ready = len(each_eng_category_list) == 3

            if is_all_csv_ready:
                print('can start to generate summary csv for this category')
                tmpPdList = list()

                # concat csv into one
                for csv in each_eng_category_list:
                    csvPath = './data_source/' + tester_fname + '/' + csv
                    # print('CSV path: {}'.format(csvPath))
                    tmpDf = pd.read_csv(csvPath, nrows = 3, usecols = useful_field_we_needs)
                    #print(tmpDf)
                    tmpPdList.append(tmpDf)

                result_df = pd.concat(tmpPdList)

                # group 3 df's value by 0, 1, 2 and calculate the average for each seconds average
                # length mush be 3 with each average lists

                tester_summary_df.at[alphabet, 'Att_0s_avg'] = round(result_df.at[0, 'Attention'].mean(), 3) if len(result_df.at[2, 'Attention']) == 3 else 'Error'
                tester_summary_df.at[alphabet, 'Att_1s_avg'] = round(result_df.at[1, 'Attention'].mean(), 3) if len(result_df.at[1, 'Attention']) == 3 else 'Error'
                tester_summary_df.at[alphabet, 'Att_2s_avg'] = round(result_df.at[2, 'Attention'].mean(), 3) if len(result_df.at[2, 'Attention']) == 3 else 'Error'
                tester_summary_df.at[alphabet, 'Med_0s_avg'] = round(result_df.at[0, 'Meditation'].mean(), 3) if len(result_df.at[0, 'Meditation']) == 3 else 'Error'
                tester_summary_df.at[alphabet, 'Med_1s_avg'] = round(result_df.at[1, 'Meditation'].mean(), 3) if len(result_df.at[1, 'Meditation']) == 3 else 'Error'
                tester_summary_df.at[alphabet, 'Med_2s_avg'] = round(result_df.at[2, 'Meditation'].mean(), 3) if len(result_df.at[2, 'Meditation']) == 3 else 'Error'

        print(tester_summary_df)

        tester_summary_df.to_csv(sum_path + '/' +  tester_fname + '.csv', encoding = 'utf-8', index = False)



if __name__ == "__main__":
   total_test_user = int(main(sys.argv[1:]))
   initial()
   generate_summary_csv()