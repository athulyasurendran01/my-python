# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
# from fancyimpute import KNN
from feature_engine.encoding import OrdinalEncoder
# importing the MICE from fancyimpute library
from fancyimpute import IterativeImputer
import copy

def ImputeCategorical(df,var_target,var_column):

    #NOTE it's assumed executed after Another imputation!!
    #it will impute all the NaN 
    
    #only consider the "selected column"
    #if only 1 column, it will turn into series, to be save set to dataframe
    df = pd.DataFrame(df[var_column]) 

    list_cat_colum = list(df.select_dtypes(include=['object', 'category']).columns)

    data_ordinal_enc = OrdinalEncoder(encoding_method='arbitrary',
            variables=None)
    #convert categorical to integer, but remove the nan    
    data_ordinal_enc.fit(df.dropna())      

    df_tmp_dictionary = data_ordinal_enc.encoder_dict_
    inverse_dictionary = copy.deepcopy(df_tmp_dictionary)

    df_encode = copy.deepcopy(df)
    
    #convert categorical to number
    for ct_dict in (df_tmp_dictionary):  
       inverse_dictionary[ct_dict] = dict(zip(df_tmp_dictionary[ct_dict].values(), df_tmp_dictionary[ct_dict].keys())) 
       df_encode[ct_dict] = df_encode[ct_dict].map(df_tmp_dictionary[ct_dict])

    df = pd.DataFrame() #release memory
    mice_imputer = IterativeImputer()
    # imputing the missing value with mice imputer
    df_encode_mice = pd.DataFrame(mice_imputer.fit_transform(df_encode))
    df_encode_mice.columns = df_encode.columns 

    #convert categorical to number
    df_result = copy.deepcopy(df_encode_mice)
    for ct_dict in (df_tmp_dictionary): 
        if ct_dict in(list_cat_colum):
           df_result[ct_dict] =  np.round(df_result[ct_dict])
        df_result[ct_dict] = df_result[ct_dict].map(inverse_dictionary[ct_dict])        

    #df_result, should not has Nan anymore, if so raise error
    if any(df_result.isnull().any()):
       raise TypeError("Error when assigning the replacement categorical")
    df_result.to_csv('Testing_file.csv')
    return df_result
    #  return df_result[[var_target]]



# #################### 1. How to use/call the function for Categorical data
# #NOTE it's assumed executed after Another imputation!!
# #it will impute all the NaN 
# Data_rawx = pd.read_csv('Bank_data_train_impute.csv',sep=";")
# lv_target = 'Geography'
# #note the lv_column also included the target
# lv_column= ['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary']
# #it will only return the "Target" column data(not all column)
# Data_update_column = rank_feature_importance(Data_rawx,lv_target,lv_column)