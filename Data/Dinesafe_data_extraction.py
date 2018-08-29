import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt

tree = ET.parse('dinesafe.xml')



root = tree.getroot()
root[0][0].text

for child in root:
    print (child.tag)
    break

col_names =[]
for attr in child:
        #print (attr.tag)
        col_names.append(attr.tag)

ROW_ID = []
ESTABLISHMENT_ID = []
INSPECTION_ID = []
ESTABLISHMENT_NAME = []
ESTABLISHMENTTYPE = []
ESTABLISHMENT_ADDRESS = []
LATITUDE =[]
LONGITUDE =[]
ESTABLISHMENT_STATUS =[]
MINIMUM_INSPECTIONS_PERYEAR =[]
INFRACTION_DETAILS =[]
INSPECTION_DATE =[]
SEVERITY =[]
ACTION =[]
COURT_OUTCOME =[]
AMOUNT_FINED= []

for child in root:
    for element in child:
        if (element.tag == col_names[0] ):   
            ROW_ID.append(element.text)
        elif (element.tag == col_names[1] ):   
            ESTABLISHMENT_ID.append(element.text)
        elif (element.tag == col_names[2] ):   
            INSPECTION_ID.append(element.text)
        elif (element.tag == col_names[3] ):   
            ESTABLISHMENT_NAME.append(element.text) 
        elif (element.tag == col_names[4] ):   
            ESTABLISHMENTTYPE.append(element.text)
        elif (element.tag == col_names[5] ):   
            ESTABLISHMENT_ADDRESS.append(element.text)
        elif (element.tag == col_names[6] ):   
            LATITUDE.append(element.text)    
        elif (element.tag == col_names[7] ):   
            LONGITUDE.append(element.text)   
        elif (element.tag == col_names[8] ):   
            ESTABLISHMENT_STATUS.append(element.text)  
        elif (element.tag == col_names[9] ):   
            MINIMUM_INSPECTIONS_PERYEAR.append(element.text)        
        elif (element.tag == col_names[10] ):   
            INFRACTION_DETAILS.append(element.text)     
        elif (element.tag == col_names[11] ):   
            INSPECTION_DATE.append(element.text)       
        elif (element.tag == col_names[12] ):   
            SEVERITY.append(element.text)      
        elif (element.tag == col_names[13] ):   
            ACTION.append(element.text)  
        elif (element.tag == col_names[14] ):   
            COURT_OUTCOME.append(element.text)    
        elif (element.tag == col_names[15] ):   
            AMOUNT_FINED.append(element.text)



df = pd.DataFrame( {'ROW_ID': ROW_ID, 'ESTABLISHMENT_ID' : ESTABLISHMENT_ID , 'INSPECTION_ID': INSPECTION_ID,\
                  'ESTABLISHMENT_NAME' : ESTABLISHMENT_NAME, 'ESTABLISHMENT_TYPE' : ESTABLISHMENTTYPE, \
                    'ESTABLISHMENT_ADDRESS' : ESTABLISHMENT_ADDRESS, 'LATITUDE': LATITUDE, 'LONGITUDE': LONGITUDE,\
                    'ESTABLISHMENT_STATUS': ESTABLISHMENT_STATUS, 'MINIMUM_INSPECTIONS_PERYEAR': MINIMUM_INSPECTIONS_PERYEAR,\
                    'INFRACTION_DETAILS': INFRACTION_DETAILS, 'INSPECTION_DATE': INSPECTION_DATE, \
                    'SEVERITY': SEVERITY, 'ACTION': ACTION, 'COURT_OUTCOME': COURT_OUTCOME,
                   'AMOUNT_FINED':AMOUNT_FINED})

df['AMOUNT_FINED'] = pd.to_numeric(df['AMOUNT_FINED'], errors ='coerce')          
df['INSPECTION_DATE'] =pd.to_datetime(df['INSPECTION_DATE'], errors = 'coerce')
df['INSP_Year'] = df['INSPECTION_DATE'].dt.year
df['INSP_Month'] = df['INSPECTION_DATE'].dt.month


#Getting Most recent inspection for each business
year_groups = df.groupby('INSP_Year')


dfs =[]
for year in year_groups:
    name, group = year
    df_y = group
    df_y = df_y.sort_values(by ='INSPECTION_DATE')
    df_y = df_y.drop_duplicates(['ESTABLISHMENT_ID'])
    dfs.append(df_y)
    
df_new = pd.concat([dfs[0],dfs[1],dfs[2]])

df_new = df_new.sort_values(by='INSPECTION_DATE', ascending = False)
df_new = df_new.drop_duplicates(['ESTABLISHMENT_ID'])
dinesafe = df_new
dinesafe.columns =map(str.lower, dinesafe.columns)

dinesafe['latitude'] = pd.to_numeric(dinesafe['latitude'])
dinesafe['longitude'] = pd.to_numeric(dinesafe['longitude'])
dinesafe['minimum_inspections_peryear'] = pd.to_numeric(dinesafe['minimum_inspections_peryear'])
dinesafe['int_lat'] = dinesafe['latitude']*(10**6)
dinesafe['int_long'] = abs(dinesafe['longitude'])*(10**6)
dinesafe['int_long_lat'] = dinesafe['int_lat'] + dinesafe['int_long']
dinesafe['new_int_long'] = dinesafe['int_long'].astype(int)
dinesafe['new_int_lat'] = dinesafe['int_lat'].astype(int)
dinesafe['new_long_lat'] = dinesafe['new_int_lat'] + dinesafe['new_int_long']
dinesafe['establishment_name'] =dinesafe['establishment_name'].str.lower()
dinesafe['establishment_address'] =dinesafe['establishment_address'].str.lower()

np.savetxt('establishment_names.csv',dinesafe['establishment_name'], '%s')
