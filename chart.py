#!/usr/bin/python3

from plotly.offline import iplot
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

df = pd.read_csv('./dist/by_alphabet/category_A.csv')

print(df)

a_0_avg = df.Att_0s_avg.mean()
a_1_avg = df.Att_1s_avg.mean()
a_2_avg = df.Att_2s_avg.mean()

m_0_avg = df.Med_0s_avg.mean()
m_1_avg = df.Med_1s_avg.mean()
m_2_avg = df.Med_2s_avg.mean()

# table = ff.create_table(df)
# iplot(table, filename='jupyter-table1')

a_df = pd.DataFrame(columns = ['seconds', 'attention_average'])
a_df.loc[0] = [0, a_0_avg]
a_df.loc[1] = [1, a_1_avg]
a_df.loc[2] = [2, a_2_avg]

print(a_df)

fig = px.line(a_df, x = 'seconds', y = 'attention_average', title = 'Average Result of all test of type A')
fig.show()