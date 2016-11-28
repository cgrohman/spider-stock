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
from datetime import datetime, timedelta, date

usholidays16 = [str(date(2016,1,1)), str(date(2016,1,18)), str(date(2016,2,15)), 
                str(date(2016,3,25)), str(date(2016,5,30)), str(date(2016,7,4)),
                str(date(2016,9,5)), str(date(2016,11,24)), str(date(2016,11,25)),
                str(date(2016,12,25)), str(date(2017,1,1)), str(date(2017,1,16)),
                str(date(2017,2,20)), str(date(2017,4,14)), str(date(2017,5,29)),
                str(date(2017,7,3)), str(date(2017,7,4)), str(date(2017,9,4)),
                str(date(2017,11,23)), str(date(2017,11,24)), str(date(2017,12,25))]

def create_date(date):
	string_date = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
	return string_date

def check_weekend(date):
	num_day = date.weekday()
	if num_day > 4:
		return True
	else:
		return False

def change_weekend(date):
	if check_weekend(date):
		num_day = date.weekday()
		date = date - timedelta(days = num_day-4)
	return date

def check_holiday(date):
	if str(date.date()) in usholidays16:
		return True
	else:
		return False 

def change_holiday(date):
	while check_holiday(date):
		date = date - timedelta(days = 1)
	return date

def get_older_dates(day):
	date = datetime.now()-timedelta(days=day)
	date_list = []
	for i in range(3):
		if i != 0:
			date = date - timedelta(days = 1)
		if check_weekend(date):
			date = change_weekend(date)
		if check_holiday(date):
			date = change_holiday(date)

		new_date = create_date(date)
		date_list.append(new_date)
	return date_list


def get_symbols(companies):
	symbols = {}
	for key,value in companies.items():
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
	for key,value in companies.items():
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
	for symbol in companies.keys():
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

sample_day = 7  #will be change to 365 days 
date_now = get_older_dates(0)
old_date = get_older_dates(sample_day)
raw_data = stock_data(old_date[0],date_now[0],tech_symbols)
shift_close1 = get_close_price(old_date[1],date_now[1],tech_symbols)
shift_close2 = get_close_price(old_date[2],date_now[2],tech_symbols)
stock_numbers = make_dataframe(raw_data)

greater = lambda x : 1 if x == True else 0     # 1 if today's price is greater than yesterday's price else 0 
stock_numbers['Compare1'] = stock_numbers['Close'] > shift_close1['Close']
stock_numbers['Compare2'] = stock_numbers['Close'] > shift_close2['Close']
stock_numbers['Compare1'] = stock_numbers['Compare1'].apply(greater)
stock_numbers['Compare2'] = stock_numbers['Compare2'].apply(greater)
stock_numbers.to_csv('stock_info.csv')            #, mode='a')
