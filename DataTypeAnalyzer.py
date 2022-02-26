#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def column_stats(df):
    output_df = pd.DataFrame(columns = ['column_name', 'data_type', 'count_missing_value', 'percentage_missing_value', 'missing_value_recommendation'])
    output_df['column_name'] = df.columns
    max_categories = round(df.shape[0]/20)
    output_df['count_missing_value'] = list(df.shape[0] - df.count())
    output_df['percentage_missing_value'] = (output_df['count_missing_value']/ df.shape[0])* 100

    for i, cols in enumerate(df.columns):
        if(df[cols].dtype == 'object'):
            if(df[cols].nunique() > max_categories):
                output_df.loc[i, 'data_type'] = 'Text'
            else:
                output_df.loc[i, 'data_type'] = 'Categorical'
        elif(df[cols].dtype == 'datetime64'):
            output_df.loc[i, 'data_type'] = 'Date'
        else:
            output_df.loc[i, 'data_type'] = 'Numeric'
            
        if(output_df.loc[i, 'percentage_missing_value'] > 30):
            output_df.loc[i, 'missing_value_recommendation'] = 'Delete column'
        elif(output_df.loc[i, 'percentage_missing_value'] > 0 and ((output_df.loc[i, 'data_type'] == 'Categorical') or (output_df.loc[i, 'data_type'] == 'Numeric'))):
            output_df.loc[i, 'missing_value_recommendation'] = 'Automatic'
        else:
            output_df.loc[i, 'missing_value_recommendation'] = 'No action required'
            
        if(output_df.loc[i, 'data_type'] == 'Text'):
            output_df.loc[i, 'missing_value_recommendation'] = 'Unable to use text'
        
        if(output_df.loc[i, 'data_type'] == 'Date'):
            output_df.loc[i, 'missing_value_recommendation'] = 'Unable to use date'
            
    return output_df