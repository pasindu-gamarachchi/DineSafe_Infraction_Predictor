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

data['infraction'] = np.where(data['severity']=='NA - Not Applicable',0,1)
establishment_groups =data.groupby('establishment_type')
insp_count_est_type =establishment_groups.count()['infraction']
inf_count_est_type =establishment_groups.sum()['infraction']
insp_count_est_type.index.values
est_types = { 'insp_count' : pd.Series(insp_count_est_type, index =insp_count_est_type.index.values ),\
            'inf_count': pd.Series(inf_count_est_type,index =insp_count_est_type.index.values  )}

df_est_types = pd.DataFrame(est_types)
df_est_types['inf_count'] = pd.to_numeric(df_est_types['inf_count'], errors ='coerce')
df_est_types['insp_count'] = pd.to_numeric(df_est_types['insp_count'], errors ='coerce')
df_est_types['No_inf_count'] = df_est_types['insp_count'] -df_est_types['inf_count']
df_est =df_est_types[df_est_types['insp_count']> 20]
df_est['p']=''
df_est['chi2']=''
total_inf =df_est_types['inf_count'].sum()
total_insp =df_est_types['insp_count'].sum()
no_inf_total = total_insp -total_inf

for i in df_est.index:
    inf_c = df_est.loc[i,'inf_count']
    insp_c = df_est.loc[i, 'No_inf_count']
    chi2, p, dof, exp =stats.chi2_contingency([[inf_c,insp_c],[total_inf,no_inf_total]])
    df_est.loc[i, 'p'] =p
    df_est.loc[i,'chi2'] =chi2

df_est.to_csv('Establishment_type_chi.csv')
