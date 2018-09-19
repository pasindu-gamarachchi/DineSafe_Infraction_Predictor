import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('Statistical_analysis_data_1.csv',
                     index_col=0)

def check_and_drop_cols(df, cols):
    for i in cols:
        if i in df.columns:
            print(i, 'dropped')
            df = df.drop(i,axis =1)
    return df
data =check_and_drop_cols(data, ['Unnamed: 0.1','label_severity'])

neigborhood_groups =data.groupby('neighborhood')
insp_count_neighb =neigborhood_groups.count()['infraction']
inf_count_neighb =neigborhood_groups.sum()['infraction']

insp_count_neighb.index.values
neighbs = { 'insp_count' : pd.Series(insp_count_neighb, index =insp_count_neighb.index.values ),\
            'inf_count': pd.Series(inf_count_neighb,index =insp_count_neighb.index.values  )}
df_neighbs = pd.DataFrame(neighbs)
df_neighbs['No_inf_count'] = df_neighbs['insp_count'] -df_neighbs['inf_count']
df_n =df_neighbs[df_neighbs['insp_count']> 20]
df_n['p']=''
df_n['chi2']=''

for i in df_n.index:
    inf_c = df_n.loc[i,'inf_count']
    insp_c = df_n.loc[i, 'No_inf_count']
    chi2, p, dof, exp =stats.chi2_contingency([[inf_c,insp_c],[total_inf,no_inf_total]])
    df_n.loc[i, 'p'] =p
    df_n.loc[i,'chi2'] =chi2

df_n.to_csv('Neighborhood_chi.csv')
