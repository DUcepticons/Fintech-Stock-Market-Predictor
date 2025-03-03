# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: raiyaan
"""

import numpy as np
import pandas as pd
import tensorflow as tf

import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline

raw_data = pd.read_csv("appledata-test.csv")

days=4 #We take features of n number of days as input and action of the nth day as output and construct a dataframe from this

list_data={}
dataframe_columns=[]

for i in range (0,days): 
    
    key1= 'Number-in-hand-'+str(i) 
    key2= 'Price-'+str(i)
    key3= 'Cash-'+str(i)
    key4= 'Return-'+str(i)
    dataframe_columns.extend([key1,key2,key3,key4])
    
    if i<days-1:
        list_data[key1] = raw_data.iloc[i:-(days-1-i),0].values.tolist() 
        list_data[key2] = raw_data.iloc[i:-(days-1-i),1].values.tolist() 
        list_data[key3] = raw_data.iloc[i:-(days-1-i),2].values.tolist() 
        list_data[key4] = raw_data.iloc[i:-(days-1-i),3].values.tolist()  
    else:
        list_data[key1] = raw_data.iloc[i:,0].values.tolist() 
        list_data[key2] = raw_data.iloc[i:,1].values.tolist() 
        list_data[key3] = raw_data.iloc[i:,2].values.tolist() 
        list_data[key4] = raw_data.iloc[i:,3].values.tolist()          

list_data['Action']= raw_data.iloc[days-1:,4].values.tolist() 
dataframe_columns.append('Action')

data = pd.DataFrame(list_data, columns = dataframe_columns)

'''
#Visualization#
corr = data.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=np.bool))


# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


'''
X = (data.iloc[:,0:-1].values).astype('float32')
#min_max_scaler = MinMaxScaler()
#X = min_max_scaler.fit_transform(X)
Y = (data.iloc[:,-1].values)


model = tf.keras.models.load_model("applestockdata.h5")
prediction = model.predict(X)

