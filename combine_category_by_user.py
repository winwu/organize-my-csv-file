# TODO: quantile

import os
import string
import re
import pandas as pd

if not os.path.exists('./data_source'):
    os.makedirs('./data_source')

# all variables
# a list for all testers folder name
userFolders = list()

# categories are named by English alphabet from A to I
englistCategoryRange = string.ascii_uppercase[:9]

# total number of testers
totalTestUser = 21


# define new columns which we need
colNames = [
    'Att_0s_avg', # Average attention value of the 0th second of all data
    'Att_1s_avg', # Average attention value of the 1st second of all data
    'Att_2s_avg', # Average attention value of the 2nd second of all data
    'Med_0s_avg', # Meditation attention value of the 0th second of all data
    'Med_1s_avg', # Meditation attention value of the 1st second of all data
    "Med_2s_avg"  # Meditation attention value of the 2nd second of all data
]

usefulFieldWeNeeds = ['Attention', 'Meditation']


for i in range(1, totalTestUser + 1):
    userFolders.append('tester' + str(i))

for userFolder in userFolders:

    # 1. create folder for each test user if not exists
    if not os.path.exists('./data_source' + '/' + userFolder):
        os.makedirs('./data_source' + '/' + userFolder)

    # 2. create summary folder for each user
    sumDirPath = './data_source' + '/' + userFolder + '/' + 'summary'
    if not os.path.exists(sumDirPath):
        os.makedirs(sumDirPath)

    # 3. init summary table df
    # define new dataFrame with 35 users
    summaryDf = pd.DataFrame(index = list(englistCategoryRange), columns = colNames)
    # set all cell value to 0 as default
    # summaryDf.fillna(0, inplace = True)

    print('---------- Processing folder: {} ----------'.format(userFolder))

    # 3. categories file names according to English alphabet (A-I)
    for upperCase in englistCategoryRange:
        csvFolder = './data_source' + '/' + userFolder

        categoryList = []
        for name in os.listdir(csvFolder):
            # search pattern like: 1-A-1.csv ~ 1-A-3.csv
            if re.match("(^[1-9]-[" + re.escape(upperCase) + "]-[1-3]).csv", name):
                categoryList.append(name)

        # update file sequance from 1 -> 2 -> 3
        categoryList = sorted(categoryList)

        print('Category {} List: {}'.format(upperCase, categoryList))

        # all groups must have three files to be continue...
        allCsvReady = len(categoryList) == 3

        if allCsvReady:
            print('can start to generate summary csv for this category')
            tmpPdList = list()

            # concat csv into one
            for csv in categoryList:
                csvPath = './data_source/' + userFolder + '/' + csv
                # print('CSV path: {}'.format(csvPath))
                tmpDf = pd.read_csv(csvPath, nrows = 3, usecols = usefulFieldWeNeeds)
                #print(tmpDf)
                tmpPdList.append(tmpDf)

            concatedDf = pd.concat(tmpPdList)

            # group 3 df's value by 0, 1, 2 and calculate the average for each seconds average
            # length mush be 3 with each average lists

            summaryDf.at[upperCase, 'Att_0s_avg'] = round(concatedDf.at[0, 'Attention'].mean(), 3) if len(concatedDf.at[2, 'Attention']) == 3 else 'Error'
            summaryDf.at[upperCase, 'Att_1s_avg'] = round(concatedDf.at[1, 'Attention'].mean(), 3) if len(concatedDf.at[1, 'Attention']) == 3 else 'Error'
            summaryDf.at[upperCase, 'Att_2s_avg'] = round(concatedDf.at[2, 'Attention'].mean(), 3) if len(concatedDf.at[2, 'Attention']) == 3 else 'Error'
            summaryDf.at[upperCase, 'Med_0s_avg'] = round(concatedDf.at[0, 'Meditation'].mean(), 3) if len(concatedDf.at[0, 'Meditation']) == 3 else 'Error'
            summaryDf.at[upperCase, 'Med_1s_avg'] = round(concatedDf.at[1, 'Meditation'].mean(), 3) if len(concatedDf.at[1, 'Meditation']) == 3 else 'Error'
            summaryDf.at[upperCase, 'Med_2s_avg'] = round(concatedDf.at[2, 'Meditation'].mean(), 3) if len(concatedDf.at[2, 'Meditation']) == 3 else 'Error'

    print(summaryDf)

    summaryDf.to_csv(sumDirPath + '/' + 'summary_'+ userFolder +'.csv', encoding='utf-8', index=False)