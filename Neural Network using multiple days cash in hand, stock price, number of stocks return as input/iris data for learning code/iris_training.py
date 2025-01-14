# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 04:27:12 2020

@author: Raiya
"""

# multi-class classification with Keras
import pandas
import tensorflow as tf

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
# load dataset
dataframe = pandas.read_csv("iris.data", header=None)
dataset = dataframe.values
X = dataset[:,0:4].astype(float)
Y = dataset[:,4]
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = tf.keras.utils.to_categorical(encoded_Y)

model = tf.keras.models.Sequential()
# define baseline model
def baseline_model():
	# create model
	
	model.add(tf.keras.layers.Dense(8, input_dim=4, activation='relu'))
	model.add(tf.keras.layers.Dense(3, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=1)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
model.save("irisdata.h5")