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
from datetime import datetime, timedelta


def get_older_date(year,month,day):
	date = datetime.now()-timedelta(days=day)
	num_day = date.weekday()
	if num_day ==  5:
		date = date - timedelta(days=1)
	elif num_day == 6:
		date = date - timedelta(days=2)
	new_date = str(date.year-year) + '-' + str(date.month) + '-' + str(date.day)
	return new_date

def get_symbols(companies):
	symbols = {}
	for key,value in companies.items()[:2]:
		try:
			symbols[key] = value
		except:
			pass
	return symbols


def stock_data(start, end,companies):
	raw_data = { 'Company': [], 
	             'High': [],
	             'Low': [],
	             'Open': [],
	             'Close': [],
	             'Volume': [],
	             'Date': []
	}
	for key,value in companies.items()[:2]:
		company = Share(key)
		company.refresh()
		data = company.get_historical(start,end)
		for item in data:
			raw_data['Company'].append(value)
			raw_data['High'].append(float(item['High']))
			raw_data['Low'].append(float(item['Low']))
			raw_data['Open'].append(float(item['Open']))
			raw_data['Close'].append(float(item['Close']))
			raw_data['Volume'].append(int(item['Volume']))
			raw_data['Date'].append(item['Date'])
	return raw_data

def make_dataframe(raw_data):
	df = pd.DataFrame({'High':raw_data['High'],
	                   'Low':raw_data['Low'],
	                   'Company': raw_data['Company'],
	                   'Open': raw_data['Open'],
	                   'Close': raw_data['Close'],
	                   'Volume': raw_data['Volume'],
	                   'Date': raw_data['Date']}, columns = raw_data.keys())
	df['Outcome'] = df['Close'] > df['Open']
	df['Ho'] = df['High'] - df['Open']
	df['Lo'] = df['Low'] - df['Open']
	df['Gain'] = df['Close'] - df['Open']

	outcome = lambda x : 1 if x == True else -1    # 1 for upday  -1 for downday
	df['Outcome'] = df['Outcome'].apply(outcome)
	return df


def get_close_price(start,end,companies):
	close_price = {'Close': [], 'Date': []}
	for symbol in companies.keys()[:2]:
		company = Share(symbol)
		company.refresh()
		data = company.get_historical(start,end)
		for item in data: 
			close_price['Close'].append(float(item['Close']))
			close_price['Date'].append(item['Date'])
	return close_price


nyse_symbols = finsym.get_nyse_symbols()
tech_companies = {item['symbol'].strip():item['company'] for item in nyse_symbols if 'Technology' in item.values()}
tech_symbols = get_symbols(tech_companies)
current_day = 1
two_day = 3
one_day = 2
sample_day = 365

date_now = get_older_date(0,0,current_day)
old_date = get_older_date(0,0,sample_day+current_day)

two_day_ago = get_older_date(0,0,two_day)
old_date_two = get_older_date(0,0,sample_day+two_day)

one_day_ago = get_older_date(0,0,one_day)
old_date_one = get_older_date(0,0,sample_day+one_day)

raw_data = stock_data(old_date,date_now,tech_symbols)
shift_close1 = get_close_price(old_date_one,one_day_ago,tech_symbols)
shift_close2 = get_close_price(old_date_two,two_day_ago,tech_symbols)
stock_numbers = make_dataframe(raw_data)
greater = lambda x : 1 if x == True else 0     # 1 if today's price is greater than yesterday's price else 0 
stock_numbers['Compare1'] = stock_numbers['Close'] > shift_close1['Close']
stock_numbers['Compare2'] = stock_numbers['Close'] > shift_close2['Close']
stock_numbers['Compare1'] = stock_numbers['Compare1'].apply(greater)
stock_numbers['Compare2'] = stock_numbers['Compare2'].apply(greater)
stock_numbers.to_csv('stock_info.csv')#, mode='a')
