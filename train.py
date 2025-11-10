#!/usr/bin/env python
# coding: utf-8

# Packages Part

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import export_text
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import root_mean_squared_error

import pickle 

from xgboost import XGBRegressor

# Data Prepration

df = pd.read_csv('data.csv')

df.columns = df.columns.str.lower()

df.divorced_earlier = (df.divorced_earlier == 'Yes').astype(int)
df.father_alive = (df.father_alive == 'Yes').astype(int)
df.mother_alive = (df.mother_alive == 'Yes').astype(int)

df.maritial_status = df.maritial_status.astype(int)

df['education_level'] = df['education_level'].str.lower().str.replace(' ','_')
df['department'] = df['department'].str.lower().str.replace(' ','_')
df['role'] = df['role'].str.lower().str.replace(' ','_')
df['employee_name'] = df['employee_name'].str.lower().str.replace(' ','_')

df['job_satisfaction'] = (df['job_satisfaction'] / 10).round(2)
df['work_life_balance'] = (df['work_life_balance'] / 10).round(2)

df = df.drop(columns=['employee_name'])

# Data Spliting

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

# Variables

eta=0.01
max_depth=3
min_child_weight=1
nthread=8
seed=1
verbosity=0
n_jobs = -1
n_estimators=200

# Traning the model with 'XGBoost'

def train(df, y, eta, max_depth, min_child_weight, n_jobs, seed, verbosity, n_estimators):

    print (f'Training the model ...')

    dicts = df.drop(columns=['job_satisfaction']).to_dict(orient='records')

    dv = DictVectorizer(sparse=False)
    X = dv.fit_transform(dicts)

    model = XGBRegressor(
        eta=eta,
        max_depth=max_depth,
        min_child_weight=min_child_weight,
        n_estimators=n_estimators,
        n_jobs=n_jobs,
    )
    model.fit(X, y)

    print('-----------------------------------')

    return dv, model

# Predict function

def predict(df, dv, model):
    dicts = df.drop(columns=['job_satisfaction'], errors='ignore').to_dict(orient='records')

    X = dv.transform(dicts)

    features = list(dv.get_feature_names_out())

    y_pred = model.predict(X)

    return y_pred

# Traning and testing the the model

dv, model = train(df_full_train, df_full_train.job_satisfaction, eta, max_depth, min_child_weight, n_jobs, seed, verbosity, n_estimators)

y_pred = predict(df_test, dv, model)
y_test = df_test.job_satisfaction

rmse = root_mean_squared_error(y_pred, y_test) * 10

print(f'RMSE of the final model is {rmse}')
print('-----------------------------------')

output_file = f'model.bin'

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

print(f'The model is saved to {output_file}')
