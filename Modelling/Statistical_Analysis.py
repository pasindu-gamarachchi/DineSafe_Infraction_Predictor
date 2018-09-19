import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Statistical_analysis_data_1.csv',
                     index_col=0)

def check_and_drop_cols(df, cols):
    for i in cols:
        if i in df.columns:
            print(i, 'dropped')
            df = df.drop(i,axis =1)
    return df
df =check_and_drop_cols(df, ['Unnamed: 0.1','label_severity'])

sevs = pd.unique(df['severity'])
df['num_severity']=''

for i in range(0,len(df)):
    if (df.loc[i,'severity']==sevs[2]):
        df.loc[i,'num_severity'] = 0
    elif (df.loc[i,'severity']==sevs[1]):
        df.loc[i,'num_severity'] = 1
    elif (df.loc[i,'severity']==sevs[0]):
        df.loc[i,'num_severity'] = 2
    elif (df.loc[i,'severity']==sevs[3]):
        df.loc[i,'num_severity'] = 3

for i in df.columns:
    a = pd.unique(df[i])
    if (0 in a and 1 in a and i[:5] == 'attrib'):
        print(i)
        df[i] = df[i].fillna(value=0);
        df[i] = pd.to_numeric(df[i], errors ='coerce') 



df_v1 =df.select_dtypes(exclude =['object'] )
r_vals =[]
p_vals =[]
features =[]
#plt.show()
for i in df_v1.columns:
    r,p = stats.spearmanr(df_v1[i],df_v1['num_severity'])
    if p < 0.05 and r > 0.1 and i != 'num_severity':
        print (i)
        print('r :','\t', r, '\t', 'p :', '\t', p)
        r_vals.append(r)
        p_vals.append(p)
        features.append(i)
        plt.figure()

        sns.regplot(df_v1[i], df_v1['num_severity']);
plt.show()
