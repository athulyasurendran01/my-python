#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
# from collections import defaultdict
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from feature_engine.selection import SelectByShuffling
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.tree import DecisionTreeClassifier, export_graphviz
# from sklearn.model_selection import cross_val_score

import warnings
warnings.filterwarnings("ignore")
from pandas.api.types import is_string_dtype
# from pandas.api.types import is_numeric_dtype
import xgboost as xgb
from feature_engine.encoding import OrdinalEncoder


from imblearn.ensemble import (
    # BalancedBaggingClassifier,
    BalancedRandomForestClassifier,
    # RUSBoostClassifier,
    # EasyEnsembleClassifier,
)

from sklearn.ensemble import (
    RandomForestClassifier,
    # BaggingClassifier,
    # AdaBoostClassifier,
)


def FeatureRank(df,ls_target,ls_data,ls_ratio='balance'):
    
    #A.Purpose: will rank feature importance based on matching Train , "Target"
    #use shuffling
    #B.Constraint : Need to defined 1 and only 1 target(Y) and feature(x)
    #if more than 1 target, will throw error
    #C.Accepted data : accepted for Classification and Regression
    #df = dataframe(data)(feature + target)
    #ls_target = list of target(but should be only 1)
    #ls_data = list of feature(X) can be >=1 features
    #D. For Categorical (Y), NO need to change to number, send as raw like "string"
    #if number will treated as regression
    
    if len(ls_target) != 1:
       raise Exception('Target(Y) should be one') #after this exit    
    
    if len(ls_data) < 1:
       raise Exception('At Least one feature required') #after this exit  
       
    #Don't allow null/nan   
    df = df.dropna()
    df.reset_index(inplace=True,drop=True)      


    x_train_ori = df[ls_data]
    y_train_ori = df[ls_target]
    
    
    lv_type = 'numeric' #datatype default target
    
    #checking datatype should be in "SERIES"
    if is_string_dtype(y_train_ori.iloc[:,0]):
       lv_type = 'category' 
        
    x_ordinal_enc = OrdinalEncoder(
        encoding_method='arbitrary',
        variables=None)

    try : # #will error if no single categorical
        x_ordinal_enc = x_ordinal_enc.fit(x_train_ori)    
        x_train_tf = x_ordinal_enc.transform(x_train_ori)
    except:   
        x_train_tf = x_train_ori        
        
    
    y_ordinal_enc = OrdinalEncoder(
            encoding_method='arbitrary',
            variables=None)
    
    try :
        y_ordinal_enc = y_ordinal_enc.fit(y_train_ori)
        y_train_tf = y_ordinal_enc.transform(y_train_ori)
    except:   
        y_train_tf = y_train_ori      
    

    if lv_type == 'numeric':
        

        y_train_tf = np.array(y_train_tf).reshape(-1)
        
        modelxgb = xgb.XGBRegressor()
        sel = SelectByShuffling(
            variables=None, # automatically examine all numerical variables
            estimator=modelxgb, # the ML model
            scoring='neg_root_mean_squared_error', # the metric to evaluate
            threshold=0,# the maximum performance drop allowed to select the feature
            cv=3, # cross validation
            random_state=1 # seed
        )
        
        
        sel.fit(x_train_tf, y_train_tf)
            
        #BIGGER better, smaller then rank lower
        rank = sel.performance_drifts_
        rank = rank.items()
        rank = list(rank)
        rank = pd.DataFrame(rank)
        rank = rank.sort_values(by=1, ascending=False)
        rank.reset_index(drop=True,inplace=True)
        rank['rank'] = rank.index + 1
        rank.rename(columns={0: "Column_name", 1: "Importance"},inplace =True)        
        #only show the rank, the "importance" scale is hidden
        rank = rank[['Column_name','rank']]        
        
        
    else:    
    

        y_train_tf = np.array(y_train_tf).reshape(-1)

        if ls_ratio=='imbalance': 
            rf = BalancedRandomForestClassifier(
                n_estimators=50,
                criterion='gini',
                max_depth=3,
                sampling_strategy='auto',
                n_jobs=4,
                random_state=1,
            )
        else:
            rf = RandomForestClassifier(
                n_estimators=50, max_depth=3, random_state=0, n_jobs=4)            

        #ASSUME Classification
        sel = SelectByShuffling(
            variables=None, # automatically examine all numerical variables
            estimator=rf, # the ML model
            scoring='roc_auc_ovo', # the metric to evaluate
            threshold=0,# the maximum performance drop allowed to select the feature
            cv=3, # cross validation
            random_state=1 # seed
        )
        
        
        sel.fit(x_train_tf, y_train_tf)

        #BIGGER better, smaller then rank lower
        rank = sel.performance_drifts_
        rank = rank.items()
        rank = list(rank)
        rank = pd.DataFrame(rank)
        rank = rank.sort_values(by=1, ascending=False)
        rank.reset_index(drop=True,inplace=True)
        rank['rank'] = rank.index + 1
        rank.rename(columns={0: "Column_name", 1: "Importance"},inplace =True)
        #only show the rank, the "importance" scale is hidden
        rank = rank[['Column_name','rank']]
    
    return rank



# #################### 1. How to use/call the function for Categorical data
# Data_rawx = pd.read_csv('Bank_data_train.csv',sep=";")
# Data_rawx = Data_rawx.dropna()
# Data_rawx.reset_index(inplace=True,drop=True)

# lv_target = ['Exited']
# lv_data = ['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary']
# #lv_type = ['numeric','category','category','numeric','numeric','numeric','numeric','category','category','numeric']

# #RANK when we think it's balance data
# result_category = rank_feature_importance(Data_rawx,lv_target,lv_data,'balance')
# print(result_category)


# #RANK when we think it's unbalance data
# result_category = rank_feature_importance(Data_rawx,lv_target,lv_data,'imbalance')
# print(result_category)

# ####################


# #################### 1. How to use/call the function for regression data
# Data_rawx = pd.read_csv('Regression_data.csv',sep=";")
# Data_rawx = Data_rawx.dropna()
# Data_rawx.reset_index(inplace=True,drop=True)

# lv_target = ['Y']
# lv_data = ['X1','X2','X3','X4']
# #lv_type = ['numeric','numeric','numeric','numeric']


# result_regression = rank_feature_importance(Data_rawx,lv_target,lv_data)
# print(result_regression)
# ####################

     