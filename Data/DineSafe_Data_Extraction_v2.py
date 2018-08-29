import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os

os.chdir('C://Users//User//Documents//FullTime_DataScience//Capstone_Project')
tree = ET.parse('..//Datasets//DineSafe//dinesafe.xml')
root = tree.getroot()

c = 0
for child in root:
        if ( c < 10):
                print (child.tag)
        c += 1

col_names =[]
for attr in child:
        print (attr.tag)
        col_names.append(attr.tag)

for attr in child:
        print(attr.tag)
        print (attr.text)


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
                    'SEVERITY': SEVERITY, 'ACTION': ACTION, 'COURT_OUTCOME': COURT_OUTCOME , 'AMOUNT_FINED' : AMOUNT_FINED})

df =df.set_index('ROW_ID')
Establishments = df.groupby('ESTABLISHMENT_ID')

df.to_csv('Complete_DataFrame.csv')
df_est = df.drop_duplicates(['ESTABLISHMENT_ID'])
df_est.to_csv('Establishments.csv')
