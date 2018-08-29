import numpy as np
import json
import os
import pandas as pd
from pandas.io.json import json_normalize


JSON_file = 'ON_bus.json'
data_dict1 = {}
data_dict2 = {}
data =[]
try:
    with open(JSON_file) as data_file:
        for line in data_file:
            data.append(json.loads(line))
except IOError as e:
    print (e)
    print ('Error')
    exit(1)


df = json_normalize(data )
df =df.set_index('business_id')
df.to_csv('Yelp_Businesses.csv',sep= ',')
