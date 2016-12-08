import math 
import pandas  as pd
from pandas.tools.plotting import scatter_matrix
from pandas import set_option
import numpy as np 
import scipy 
import matplotlib.pyplot as plt
from numpy import set_printoptions
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

names = ['Volume','Company','High',
         'Low,Date','Close','Open','Outcome',
         'Ho','Lo','Gain','Compare1','Compare2'
         ]

data = pd.read_csv('stock_info.csv')

# set_option('display.width',100)

set_option('precision',3)

#sort the dataframe descending

data_size = data.shape

peek = data.head(20)

var_type = data.dtypes

#Descritptive Statistics

description = data.describe()

outcome = data.groupby('Outcome').size()

one_dayago = data.groupby('Compare1').size()

two_dayago = data.groupby('Compare2').size()

correlations = data.corr(method = 'pearson')

skew = data.skew()


#Visualization

data.hist()


data.plot(kind='density',subplots=True, layout =(4,3), sharex = False)


data.plot(kind = 'box', subplots = True, layout=(4,3), sharex = False, sharey = False)


#correlation matrix
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlations , vmin=-1, vmax=1)

fig.colorbar(cax)
ticks = np.arange(0,12,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(names)
ax.set_yticklabels(names)

scatter_matrix(data)
plt.show()

#data transformation
numpy.set_printoptions(precision=3)
values = data.values
attributes = values[:,0:11]
predict = values[:,11]
minmax_scaler = MinMaxScaler(feature_range = (0,1))
standard_scaler = StandardScaler.fit(attributes)
minmax_scaled_attributes = scaler.fit_transform(attributes)
standar_scaled_attributes = standard_scaler.transform(attributes)


#feature selection
test = SelectKBest(score_func = chi2, k = 3)
fit = test.fit(attributes,predict)
weight_features_value = fit.scores_
features = fit.transform(attributes)







