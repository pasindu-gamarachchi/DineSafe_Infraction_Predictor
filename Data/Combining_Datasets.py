import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import math

dinesafe = pd.read_csv('dinesafe.csv')
dinesafe['establishment_name'] =dinesafe['establishment_name'].str.lower()
dinesafe['establishment_address'] =dinesafe['establishment_address'].str.lower()
dinesafe['int_lat'] = dinesafe['latitude']*(10**6)
dinesafe['int_lat'] = dinesafe['int_lat'].astype(int)
dinesafe['int_long'] = dinesafe['longitude']*-(10**6)
dinesafe['int_long'] = dinesafe['int_long'].astype(int)

Yelp_data = pd.read_csv('Yelp_data_filt_v2.csv')

cities_to_remove =['Ajax','Ansnorveldt', 'Anthem', 'Beeton', 'Bolton', 'Bradford',  'Bradford West Gwillimbury',\
                 'Brampton','Bridgeville', 'Brooklin', 'Caledon', 'Caledon East','Canonsburg', 'Chardon','Clarkson','Concord','Coraopolis',  'East Ajax', 'East Gwilimbury', 'Gormley', 'Huntersville',\
                  'Kannapolis', 'Kent', 'King City', 'Kingussie','Kleinburg',  'Laval','Ludwigsburg',\
                  'Malton','Maple', 'Mentor-on-the-Lake', 'Midlothian','Missisauga', 'Mississauaga', 'Mississauga',\
                  'Nobleton', 'Oak Ridges', 'Oakridges', 'Oakville','Outremont','Painesville', 'Port Credit','Rantoul','River Drive Park', 'Russellton','Sainte-Julie','Schomberg','Scottsdale',\
                  'Stouffville','Stoughton', 'Streetsboro', 'Streetsville','Strongsville', 'Stuttgart',\
                 'Thornhil', 'Unionville', 'Vaughn City','WICKLIFFE', 'Waunakee','Whiitby', 'Whitby',\
                  'Whitchurch-Stouffville','Whtiby', 'Woodbridge', 'Woodbridge (Vaughan)','oakville']

Yelp_data_v2 = Yelp_data

Yelp_data_v2['int_lat'] = Yelp_data_v2['latitude']*(10**6)
Yelp_data_v2['int_lat'] = Yelp_data_v2['int_lat'].astype(int)
Yelp_data_v2['int_long'] = Yelp_data_v2['longitude']*-(10**6)
Yelp_data_v2['int_long'] = Yelp_data_v2['int_long'].astype(int)

ds_min_lat = np.min(dinesafe['int_lat'])
ds_max_lat = np.max(dinesafe['int_lat'])

ds_min_long = np.min(dinesafe['int_long'])
ds_max_long = np.max(dinesafe['int_long'])

err_lat_ind = []
for i in range(0, len(Yelp_data_v2)):
    if ( Yelp_data_v2.loc[i,'int_lat'] < ds_min_lat or Yelp_data_v2.loc[i,'int_lat'] > ds_max_lat):
        
        Yelp_data_v2 = Yelp_data_v2.drop(i)

Yelp_data_v2 =Yelp_data_v2.reset_index()

for i in range(0, len(Yelp_data_v2)):
    if ( Yelp_data_v2.loc[i,'int_long'] <= ds_min_long or Yelp_data_v2.loc[i,'int_long'] >= ds_max_long):
    
        
        Yelp_data_v2 = Yelp_data_v2.drop(i)

Yelp_data_v2 =Yelp_data_v2.reset_index()
Yelp_data_v2['est_id'] =''
tol = 1000


inds_yelp =[]
inds_ds =[]
for i in range(0,len(Yelp_data_v2)):
    for  j  in range (0, len(dinesafe)):
        if ( abs(Yelp_data_v2.loc[i, 'int_lat'] - dinesafe.loc[j, 'int_lat'] )< tol and
            abs(Yelp_data_v2.loc[i, 'int_long'] - dinesafe.loc[j, 'int_long'] )<tol) and \
            Yelp_data_v2.loc[i,'name'][:5] == dinesafe.loc[j,'establishment_name'][:5] :
            
            Yelp_data_v2.loc[i,'est_id'] = dinesafe.loc[j,'establishment_id']
            inds_yelp.append(i)
            inds_ds.append(j)
    if (i%1000==0):
        print(i)

Yelp_data_v2['name'] =Yelp_data_v2['name'].str.lower()
Yelp_data_v2['name'] =Yelp_data_v2['name'].str.strip()
Yelp_data_v2['address'] =Yelp_data_v2['address'].str.strip()
Yelp_data_v2['address'] =Yelp_data_v2['address'].str.lower()

Yelp_data_v2.to_csv('Yelp_data_w_est_id.csv')

dinesafe_v2 = dinesafe.set_index('establishment_id')

Yelp_data_v3 = Yelp_data_v2
Yelp_data_v3 = Yelp_data_v3.rename(columns ={'est_id':'establishment_id' })
df_merged = pd.merge(dinesafe, Yelp_data_v3, on ='establishment_id')

df_merged.to_csv('df_merged.csv')
df_merged_v2 = df_merged

inds_2_drop = [18, 41, 55, 94, 207, 295, 328, 344, 374, 568, 570, 622, 660, 662, 667, 695, 724, 725, 762, 900, \
               937, 971, 1080, 1096, 1104, 1166, 1176, 1188, 1248,1249, 1323, 1326, 1345, 1350, 1359,1453,1455,1536,\
               1584,1643, 1701,1732, 1836, 1858, 1902, 1920, 2006, 2039, 2043, 2091, 2141, 2145, 2205, 22260,2261, 2309,\
               2310, 2322, 2392, 2406, 2409, 2468, 2482, 2488, 2490,2491, 2498, 2506, 2549, 2576, 2596, 2709, 2722, 2994,\
               3112,3123,3125, 3164, 3165, 3186,3187, 3415, 3555, 3586, 3619,3620, 3667, 3675, 3693, 3763, 3793, 3802, 3827,\
               3841, 3882,3883, 3957, 3958, 3967, 3980, 4067, 4085, 4105, 4134, 4169, 4170,4171, 4258,4259, 4261, 4442,4538,\
               4545, 4625, 4678, 4686,4687, 4688, 4719, 4732, 4750, 4825,4834, 4851, 4902, 4914, 4928,4929, 4998, 5011, 5022,\
               5172,5185, 5191, 5198, 5204, 5295, 5385, 5399, 5483, 5500,5501, 5520,5531, 5533, 5609, 5613, 5666, 5667, 5668,\
               5698, 5745]

for i in range(0, len(inds_2_drop)):
    df_merged_v2 = df_merged_v2.drop(i)

df_merged_v2.to_csv('df_merged_v2.csv')


dinesafe['establishment_name'] =dinesafe['establishment_name'].str.strip()



