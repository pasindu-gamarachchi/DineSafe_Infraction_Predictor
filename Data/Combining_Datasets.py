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

