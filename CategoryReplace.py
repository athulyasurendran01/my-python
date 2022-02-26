#!/usr/bin/env python
# coding: utf-8

import numpy as np

#retrieve distinct value of a column
def get_value(dataframe, colname):
    df_temp = dataframe.copy()
    return np.sort(df_temp[colname].unique())

#replace value with other value only applys to categorical data
def replace_value(dataframe, colname, ls_value, replace):
    df_temp = dataframe.copy()
    df_temp[colname] = df_temp[colname].replace(ls_value,replace)
    return df_temp
