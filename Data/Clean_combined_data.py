import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('df_merged_v2.csv')

cols_2_drop =['Column','Unnamed: 0_x','action','court_outcome','establishment_address','establishment_status',\
             'inspection_id','long_lat_x','int_lat_x','int_long_x', 'int_long_lat_x',  'new_int_long', \
              'new_int_lat',  'level_0',  'index', 'Unnamed: 0_y', 'business_id', 'address', 'name',  'postal_code',\
              'state', 'long_lat_y', 'int_lat_y', 'int_long_y',  'int_long_lat_y', 'name_match', 'amount_fined',\
              'new_long_lat', 'latitude_y', 'longitude_y'
             ]

def check_and_drop_cols(df, cols):
    for i in cols:
        if i in df.columns:
            df = df.drop(i,axis =1)
    return df
df = check_and_drop_cols(df, cols_2_drop)
df_v2 = df.copy()

df_v2['Monday Start_time'] =df_v2['hours.Monday'].str[:2].str.replace(":"," ")
df_v2['Tuesday Start_time'] =df_v2['hours.Tuesday'].str[:2].str.replace(":"," ")
df_v2['Wednesday Start_time'] =df_v2['hours.Wednesday'].str[:2].str.replace(":"," ")
df_v2['Thursday Start_time'] =df_v2['hours.Thursday'].str[:2].str.replace(":"," ")
df_v2['Friday Start_time'] =df_v2['hours.Friday'].str[:2].str.replace(":"," ")
df_v2['Saturday Start_time'] =df_v2['hours.Saturday'].str[:2].str.replace(":"," ")
df_v2['Sunday Start_time'] =df_v2['hours.Sunday'].str[:2].str.replace(":"," ")

df_v2['Monday Close_time']=df_v2['hours.Monday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Tuesday Close_time']=df_v2['hours.Tuesday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Wednesday Close_time']=df_v2['hours.Wednesday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Thursday Close_time']=df_v2['hours.Thursday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Friday Close_time']=df_v2['hours.Friday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Saturday Close_time']=df_v2['hours.Saturday'].str[-5:].str.replace("-"," ").str[:2]
df_v2['Sunday Close_time']=df_v2['hours.Sunday'].str[-5:].str.replace("-"," ").str[:2]

df_v2['inspection_date'] =pd.to_datetime(df_v2['inspection_date'], errors = 'coerce')
df_v2['insp_day']=df_v2['inspection_date'].dt.day
df_v2['insp_day_of_week']=df_v2['inspection_date'].dt.dayofweek

df_v3 = df_v2.copy()

cols_2_drop_new = ['establishment_name', 'infraction_details', 'categories']

df_v3 = check_and_drop_cols(df_v3, cols_2_drop_new)

for i in df_v3.columns:
    a = pd.unique(df_v3[i])
    if (0 in a and 1 in a):
        df_v3[i] = df_v3[i].fillna(value=0);


## Dummy Vars
establishment_type_dummies = pd.get_dummies(df_v3['establishment_type'], prefix ='establishment_type')
ages_allowed_dummies = pd.get_dummies(df_v3['attributes.AgesAllowed'], prefix ='ages_allowed')
alcohol_dummies = pd.get_dummies(df_v3['attributes.Alcohol'], prefix ='Alcohol')
Noise_lvl_dummies = pd.get_dummies(df_v3['attributes.NoiseLevel'], prefix ='Noise_lvl')
attire_dummies = pd.get_dummies(df_v3['attributes.RestaurantsAttire'], prefix ='Attire')
smoking_dummies =pd.get_dummies(df_v3['attributes.Smoking'], prefix ='Smoking')
wifi_dummies = pd.get_dummies(df_v3['attributes.WiFi'], prefix ='WiFi')
city_dummies = pd.get_dummies(df_v3['city'], prefix ='city')
neighborhood_dummies = pd.get_dummies(df_v3['neighborhood'], prefix ='neighborhood')

#print(df_v3.columns[df_v3.isna().any()].tolist())
df_v4 = df_v3.copy()

df_v4['severity'] = df_v4['severity'].fillna(value='NA - Not Applicable')
le = LabelEncoder()
df_v4['label_severity']=le.fit_transform(df_v4.severity.values)

cols_2_drop_3 =['hours.Friday','hours.Monday','hours.Saturday','hours.Sunday', \
              'hours.Thursday','hours.Tuesday','hours.Wednesday']
df_v4 = check_and_drop_cols(df_v4, cols_2_drop_3)


df_v4['Monday Start_time'] = pd.to_numeric(df_v4['Monday Start_time'], errors ='coerce')
df_v4['Tuesday Start_time'] = pd.to_numeric(df_v4['Tuesday Start_time'], errors ='coerce')
df_v4['Wednesday Start_time'] = pd.to_numeric(df_v4['Wednesday Start_time'], errors ='coerce')
df_v4['Thursday Start_time'] = pd.to_numeric(df_v4['Thursday Start_time'], errors ='coerce')
df_v4['Friday Start_time'] = pd.to_numeric(df_v4['Friday Start_time'], errors ='coerce')
df_v4['Saturday Start_time'] = pd.to_numeric(df_v4['Saturday Start_time'], errors ='coerce')
df_v4['Sunday Start_time'] = pd.to_numeric(df_v4['Sunday Start_time'], errors ='coerce')

df_v4['Monday Close_time'] = pd.to_numeric(df_v4['Monday Close_time'], errors ='coerce')
df_v4['Tuesday Close_time'] = pd.to_numeric(df_v4['Tuesday Close_time'], errors ='coerce')
df_v4['Wednesday Close_time'] = pd.to_numeric(df_v4['Wednesday Close_time'], errors ='coerce')
df_v4['Thursday Close_time'] = pd.to_numeric(df_v4['Thursday Close_time'], errors ='coerce')
df_v4['Friday Close_time'] = pd.to_numeric(df_v4['Friday Close_time'], errors ='coerce')
df_v4['Saturday Close_time'] = pd.to_numeric(df_v4['Saturday Close_time'], errors ='coerce')
df_v4['Sunday Close_time'] = pd.to_numeric(df_v4['Sunday Close_time'], errors ='coerce')

cols_2_drop_4 =['attributes.AgesAllowed','attributes.Alcohol','attributes.NoiseLevel','attributes.RestaurantsAttire', \
              'attributes.Smoking','attributes.WiFi','city','neighborhood', 'establishment_type']

df_v4 = check_and_drop_cols(df_v4, cols_2_drop_4)
df_v4['attributes.RestaurantsPriceRange2'] = df['attributes.RestaurantsPriceRange2']
df_v4['attributes.RestaurantsPriceRange2'] = df_v4['attributes.RestaurantsPriceRange2'].fillna(value=np.mean(df_v4['attributes.RestaurantsPriceRange2']));


## Fill Missing values for starting and closing times with most reasonable values
days =['Monday Start_time', 'Tuesday Start_time', 'Wednesday Start_time',
       'Thursday Start_time', 'Friday Start_time', 'Saturday Start_time',
       'Sunday Start_time']
for day in days: 
    print(day)
    for i in range(0,len(df_v4)):
        if (pd.isna(df_v4.loc[i, day]) ): ## change to j
            #print(i)
            df_v4.loc[i,day] = df_v4.loc[i,'Tuesday Start_time']
            if (pd.isna(df_v4.loc[i, 'Tuesday Start_time']) ):
                df_v4.loc[i,day] = df_v4.loc[i,'Wednesday Start_time']
                if (pd.isna(df_v4.loc[i, 'Wednesday Start_time']) ):
                    df_v4.loc[i,day] = df_v4.loc[i,'Thursday Start_time']
                    if (pd.isna(df_v4.loc[i, 'Thursday Start_time']) ):
                        df_v4.loc[i,day] = df_v4.loc[i,'Friday Start_time']
                        if (pd.isna(df_v4.loc[i, 'Friday Start_time']) ):
                            df_v4.loc[i,day] = df_v4.loc[i,'Saturday Start_time']
                            if (pd.isna(df_v4.loc[i, 'Saturday Start_time']) ):
                                df_v4.loc[i,day] = df_v4.loc[i,'Sunday Start_time']
                                if (pd.isna(df_v4.loc[i, 'Sunday Start_time']) ):
                                    df_v4.loc[i,day] = np.mean(df_v4[day])

days =['Monday Close_time', 'Tuesday Close_time', 'Wednesday Close_time',
       'Thursday Close_time', 'Friday Close_time', 'Saturday Close_time',
       'Sunday Close_time']
for day in days: 
    print(day)
    for i in range(0,len(df_v4)):
        if (pd.isna(df_v4.loc[i, day]) ): ## change to j
            #print(i)
            df_v4.loc[i,day] = df_v4.loc[i,days[1]]
            if (pd.isna(df_v4.loc[i, days[1]]) ):
                df_v4.loc[i,day] = df_v4.loc[i,days[2]]
                if (pd.isna(df_v4.loc[i, days[2]]) ):
                    df_v4.loc[i,day] = df_v4.loc[i,days[3]]
                    if (pd.isna(df_v4.loc[i, days[3]]) ):
                        df_v4.loc[i,day] = df_v4.loc[i,days[4]]
                        if (pd.isna(df_v4.loc[i, days[4]]) ):
                            df_v4.loc[i,day] = df_v4.loc[i,days[5]]
                            if (pd.isna(df_v4.loc[i, days[5]]) ):
                                df_v4.loc[i,day] = df_v4.loc[i,days[6]]
                                if (pd.isna(df_v4.loc[i, days[6]]) ):
                                    df_v4.loc[i,day] = np.mean(df_v4[day])

df_v5 = pd.concat([df_v4,establishment_type_dummies, ages_allowed_dummies, alcohol_dummies,\
                  Noise_lvl_dummies, attire_dummies, smoking_dummies, wifi_dummies, city_dummies, neighborhood_dummies], axis =1)

cols_2_drop_5 = df_v5.columns[df_v5.isna().any()].tolist()
df_v5 = check_and_drop_cols(df_v5, cols_2_drop_5)
df_v5.to_csv('Cleaned_Data.csv')
df_v4 = check_and_drop_cols(df_v4, cols_2_drop_5)
df_v4.to_csv('Statistical_analysis_data_1.csv')
