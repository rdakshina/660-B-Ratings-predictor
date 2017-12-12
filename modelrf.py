# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 15:53:35 2017

Description: Apply Random forest classifier to predict ratings

Before binning: 0.4394124847
After binning: 0.707466340269
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.cross_validation import train_test_split

#read csv using pandas
df = pd.read_csv('Clean.csv')
#keep only required columns
df = df[['Avg_Rest_Rating', 'Rating','Avg_User_rating']]

df['Avg_Rest_Rating'] = df['Avg_Rest_Rating'].str.extract('(\d+)').astype(float)
df['Rating'] = df['Rating'].str.extract('(\d+)').astype(float)

#binning the ratings as positive(1), neutral(0), negative(-1)
df1 = df.copy()
for i in df.columns[0:2]:
    df1.loc[df1[i]<3,i] = -1
    df1.loc[df1[i]==3,i] = 0
    df1.loc[df1[i]>3,i] = 1

#predict y(rating) based on x(Avg_Rest_Rating and Avg_User_rating)
X = df1.iloc[:,[0,2]]
y = df1.iloc[:,1]

#set training set to 75% of total
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 5)

#apply radom forest classifier
clf = RandomForestClassifier(max_depth=1000, max_features='log2', min_samples_split=200, random_state=150, n_estimators=1500, criterion='entropy')

#fit the model to training set
clf.fit(X_train, y_train)

#predict using the trained model
pred=clf.predict(X_test)

#check accuracy of prediction
print (accuracy_score(pred,y_test))
