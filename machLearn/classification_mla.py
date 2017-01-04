import math 
import pandas  as pd
from pandas.tools.plotting import scatter_matrix
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

plt.style.use('ggplot')
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60) 

file_name = 'stock_info.csv'
names = ['Volume','Company','High',
         'Low,Date','Close','Open','Outcome',
         'Ho','Lo','Gain','Compare1','Compare2'
         ]

data = pd.read_csv(file_name)

#This column does not belong in the dataframe
data = data.drop('Unnamed: 0',1)  


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


# #Visualization
# data.hist()
# data.plot(kind='density',subplots=True, layout =(4,3), sharex = False)
# data.plot(kind = 'box', subplots = True, layout=(4,3), sharex = False, sharey = False)

# #correlation matrix
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.matshow(correlations , vmin=-1, vmax=1)

# fig.colorbar(cax)
# ticks = np.arange(0,12,1)
# ax.set_xticks(ticks)
# ax.set_yticks(ticks)
# ax.set_xticklabels(names)
# ax.set_yticklabels(names)

# scatter_matrix(data)
# plt.show()

array = data.values

X = array[:,:10]
Y = array[:,11:]

test_size = 0.33

seed = 7

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,
	test_size = test_size, random_state=seed)

models = []
models.append(( 'LR' , LogisticRegression()))
models.append(( 'LDA' , LinearDiscriminantAnalysis()))
models.append(( 'KNN' , KNeighborsClassifier()))
models.append(( 'CART' , DecisionTreeClassifier()))
models.append(( 'NB' , GaussianNB()))
models.append(( 'SVM' , SVC()))

# # evaluate each model in turn
# results = []
# names = []
# scoring = 'accuracy'
# for name, model in models:
#   kfold = KFold(n_splits=10, random_state=seed)
#   cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring = scoring )
#   results.append(cv_results)
#   names.append(name)
#   msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#   print(msg)


# # Compare Algorithms
# fig = plt.figure()
# fig.suptitle( 'Algorithm Comparison')
# ax = fig.add_subplot(111)
# plt.boxplot(results)
# ax.set_xticklabels(names)
# plt.show()









