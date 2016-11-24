'''
This stock_info.py grabs the tech company information from yahoo fiance
and creates a csv file 
The csv file contains one month of data from yahoo fiance
'''

from yahoo_finance import Share
from pprint import pprint
import finsymbols as finsym
import pandas as pd
import numpy as np
from datetime import datetime


nyse = finsym.get_nyse_symbols()

tech_company = {item['symbol'].strip():item['company'] for item in nyse if 'Technology' in item.values()}

raw_data = {
             'Company': [],
             'High':  [],
             'Low':   [],
             'Open':  [],
             'Close': [],
            }

date = datetime.now()
date_now = str(date.year) + '-' + str(date.month) + '-' + str(date.day-10)
one_months_ago = str(date.year) + '-' + str(date.month-1) + '-' + str(date.day)


not_found = []

for key,value in tech_company.items():
	try:
		company = Share(key)
		data = company.get_historical(one_months_ago,date_now)
		for item in data:
			raw_data['Company'].append(value)
			raw_data['High'].append(item['High'])
			raw_data['Low'].append(item['Low'])
			raw_data['Open'].append(item['Open'])
			raw_data['Close'].append(item['Close'])
	except:
		not_found.append(key)       #these are symbols not found in the yahoo fiance 
        pass

df = pd.DataFrame({'High':raw_data['High'],
	               'Low':raw_data['Low'],
	               'Company': raw_data['Company'],
	               'Open': raw_data['Open'],
	               'Close': raw_data['Close']}, columns = raw_data.keys())

df.to_csv('stock_info.csv', mode='a')
