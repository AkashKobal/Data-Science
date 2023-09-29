# -*- coding: utf-8 -*-
"""BigMartSalesPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RV_hn0jHLj06lK_LecF2JydotbQFyHta

Understanding the Big Mart Sales Prediction Dataset

1.ItemIdentifier ---- Unique product ID

2.ItemWeight ---- Weight of product

3.ItemFatContent ---- Whether the product is low fat or not

4.ItemVisibility ---- The % of the total display area of all products in a store allocated to the particular product

5.ItemType ---- The category to which the product belongs

6.ItemMRP ---- Maximum Retail Price (list price) of the product

7.OutletIdentifier ---- Unique store ID

8.OutletEstablishmentYear ---- The year in which the store was established

9.OutletSize ---- The size of the store in terms of ground area covered

10.OutletLocationType ---- The type of city in which the store is located

11.OutletType ---- Whether the outlet is just a grocery store or some sort of supermarket

12.ItemOutletSales ---- sales of the product in the particular store. This is the outcome variable to be predicted.
"""



"""**Uploading the Dataset in the Google Colab**"""



"""**Importing the Libraries**"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics



"""**Reading Data and Processing**"""

#Loading the data from csv file
bmdata=pd.read_csv('/content/big_mart_sales.csv')

#display the first 5 rows of the dataframe
bmdata.head()

#displaying the shape of the dataset
bmdata.shape

#displaying the info about the dataset
bmdata.info()

#checking the missing values
bmdata.isnull().sum()



"""**Handling Missing Values**"""

#mean of 'Item_Weight' column
bmdata['Item_Weight'].mean()

#filling the missing values in Item_Weight column
bmdata['Item_Weight'].fillna(bmdata['Item_Weight'].mean(),inplace=True)

#mode of 'Outlet_Size' column
bmdata['Outlet_Size'].mode()

#filling the missing values in Outlet_Size column
mode_of_Outlet_size=bmdata.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x:x.mode()[0]))

print(mode_of_Outlet_size)

miss_values=bmdata['Outlet_Size'].isnull()

miss_values

bmdata.loc[miss_values,'Outlet_Size']=bmdata.loc[miss_values,'Outlet_Type'].apply(lambda x: mode_of_Outlet_size[x])

bmdata.isnull().sum()



"""**Data Analysis and Visualization**"""

bmdata.describe()



"""**Data Visualization-Numerical and Categorical Features**"""

sns.set()

#Item_Weight Distribution
plt.figure(figsize=(8,6))
sns.distplot(bmdata['Item_Weight'])
plt.show()

#Item_Visibility Distribution

plt.figure(figsize=(8,6))
sns.distplot(bmdata['Item_Visibility'])
plt.show()

#Item_MRP Distribution
plt.figure(figsize=(8,6))
sns.distplot(bmdata['Item_MRP'])
plt.show()

#Item_Outlet_Sales Distribution
plt.figure(figsize=(8,6))
sns.distplot(bmdata['Item_Outlet_Sales'])
plt.show()

#Outlet_Establishment_Year column
plt.figure(figsize=(8,6))
sns.countplot(x='Outlet_Establishment_Year',data=bmdata)
plt.show()

#Item_Fat_Content column
plt.figure(figsize=(8,6))
sns.countplot(x='Item_Fat_Content',data=bmdata)
plt.show()

#Outlet_Size column
plt.figure(figsize=(8,6))
sns.countplot(x='Outlet_Size',data=bmdata)
plt.show()



"""**Data Preprocessing**"""

bmdata.head()

bmdata['Item_Fat_Content'].value_counts()

bmdata.replace({'Item_Fat_Content':{'low fat':'Low FaT','LF':'Low Fat','Low FAT':'Low Fat','reg':'Regular'}},inplace=True)

bmdata['Item_Fat_Content'].value_counts()



"""**Label Encoding**"""

encoder=LabelEncoder()

#encoding Item_Identifier
bmdata['Item_Identifier']=encoder.fit_transform(bmdata['Item_Identifier'])

#encoding Item_Fat_Content
bmdata['Item_Fat_Content']=encoder.fit_transform(bmdata['Item_Fat_Content'])

#encoding Item_Type
bmdata['Item_Type']=encoder.fit_transform(bmdata['Item_Type'])

#encoding Outlet_Identifier
bmdata['Outlet_Identifier']=encoder.fit_transform(bmdata['Outlet_Identifier'])

#encoding Outlet_Size
bmdata['Outlet_Size']=encoder.fit_transform(bmdata['Outlet_Size'])

#encoding Outlet_Location_Type
bmdata['Outlet_Location_Type']=encoder.fit_transform(bmdata['Outlet_Location_Type'])

#encoding Outlet_Type
bmdata['Outlet_Type']=encoder.fit_transform(bmdata['Outlet_Type'])

bmdata.head()



"""**Splitting Data into Features and Target**"""

X=bmdata.drop(columns='Item_Outlet_Sales',axis=1)
Y=bmdata['Item_Outlet_Sales']

X

Y



"""**Splitting Data into Training and Testing Data**"""

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=2)

print(X_train.shape,X_test.shape)



"""**Model Training and Evaluation-XGBoost Regressor**"""

model=XGBRegressor()

model.fit(X_train,Y_train)

#predicting
train_data_predict=model.predict(X_train)

#RSquared value
r2_train=metrics.r2_score(Y_train,train_data_predict)

r2_train

test_data_predict=model.predict(X_test)

r2_test=metrics.r2_score(Y_test,test_data_predict)

r2_test


