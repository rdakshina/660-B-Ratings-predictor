# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:01:05 2017

Description: Apply multinomial NB classifier to predict ratings

Before binning: 0.359853121175
After binning: 0.690330477356

"""

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB

#read csv using pandas
df = pd.read_csv('Clean.csv')
#keep only required columns
df = df[['Avg_Rest_Rating', 'Rating','Avg_User_rating']]

df['Avg_Rest_Rating'] = df['Avg_Rest_Rating'].str.extract('(\d+)').astype(float)
df['Rating'] = df['Rating'].str.extract('(\d+)').astype(float)


#binning the ratings as positive(1), neutral(2), negative(3)
#because Input X must be non-negative
df1 = df.copy()
for i in df.columns[0:2]:
    df1.loc[df1[i]<3,i] = 1
    df1.loc[df1[i]==3,i] = 2
    df1.loc[df1[i]>3,i] = 3

#predict y(rating) based on x(Avg_Rest_Rating and Avg_User_rating)
X = df1.iloc[:,[0,2]]
y = df1.iloc[:,1]

#set training set to 75% of total
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 5)

#apply multinomial Naive Bayes
nb = MultinomialNB()

#fit the model to training data
nb.fit(X_train, y_train)

#predict using the trained model
y_pred = nb.predict(X_test)

#check accuracy of prediction
print (accuracy_score(y_pred, y_test))