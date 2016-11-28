import math 
import pandas  as pd
import numpy as np 
import scipy 
import matplotlib.pyplot as plt

#header_names = []
data_set = pd.read_cs('stock_info.csv')

# set_option('display.width',100)
set_option('precision',3)

#delete the name column 
#sort the dataframe descending

data_size = data.shape

peek = data.head(20)

var_type = data.dtypes

description = data.describe()


