#!/usr/bin/python3
import os
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from helpers.log_colors import log_colors
from helpers.gconfig import gconfig

boxplot_color = {
    'boxes': 'DarkGreen',
    'whiskers': 'DarkOrange',
    'medians': 'DarkBlue',
    'caps': 'Gray'
}

def gen_bloxplot_and_linechart():

    for alphabet in gconfig.english_type_range:
        csv_path = os.path.join('./dist/by_alphabet/type_' + str(alphabet) + '.csv')
        
        if not os.path.exists(csv_path):
            print('{}[Warning]\n: {}\'not exists.{}'.format(log_colors.WARNING, csv_path, log_colors.ENDC))
        
        else:
            df = pd.read_csv(csv_path, usecols=['tester', 'att_0s_avg_23', 'att_1s_avg_23', 'att_2s_avg_23', 'med_0s_avg_23', 'med_1s_avg_23', 'med_2s_avg_23'])
            print('----------- {} -------------\n'.format(str(csv_path)))
        
            # 重新命名欄位，使可讀性較高
            df.columns = ['tester', 'Att 0s', 'Att 1s', 'Att 2s', 'Med 0s', 'Med 1s', 'Med 2s']
            print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
            
            

            # boxplot
            boxchart_att = df[['Att 0s', 'Att 1s', 'Att 2s']].plot.box(ylim = (10, 100), color = boxplot_color, sym = 'r+', grid = True)
            plt.title('category ' + alphabet + ': Attention Average boxplot')
            plt.savefig('./dist/boxplot/type_' + alphabet + '_attention.png', format="png", dpi = 200)
            plt.close()

            boxchart_med = df[['Med 0s', 'Med 1s', 'Med 2s']].plot.box(ylim = (10, 100), color = boxplot_color, sym = 'r+', grid = True)
            plt.title('category ' + alphabet + ': Meditation Average boxplot')
            plt.savefig('./dist/boxplot/type_' + alphabet + '_meditation.png', format="png", dpi = 200)
            plt.close()


            # lineplot
            att_df_line = df[['Att 0s', 'Att 1s', 'Att 2s']]
            att_df_line.columns = ['0s', '1s', '2s']
            att_df_line = att_df_line.mean()
            print('Att type: {} 最後兩次平均值\n{}\n'.format(str(alphabet), att_df_line))
            

            med_df_line = df[['Med 0s', 'Med 1s', 'Med 2s']]
            med_df_line.columns = ['0s', '1s', '2s']
            med_df_line = med_df_line.mean()
            print('Med type: {} 最後兩次平均值\n{}\n'.format(str(alphabet), med_df_line))

            att_df_line.plot.line(subplots=True, color=['red'], ylim = (10, 100), grid = True)
            med_df_line.plot(color=['green'])
            plt.title('category ' + alphabet + ': Attention and Meditation Average')
            plt.savefig('./dist/line_chart/type_' + alphabet + '.png', format="png", dpi = 200)
            plt.close()

if __name__ == "__main__":
    gen_bloxplot_and_linechart()

    # gen_line_chart()