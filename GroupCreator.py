#!/usr/bin/env python
# coding: utf-8

#making group from a specified column name, threshold in a dataframe
def FC_CreateGroup(DataFrame, NumericColumnName, Threshold):
    #get the specified columnname from the DataFrame
    newdf = DataFrame[[NumericColumnName]]
    #remove the threshold duplicate value
    Threshold = sorted(list(dict.fromkeys(Threshold)))

    #get the threshold length, min and max value
    _bin = len(Threshold)
    _min = min(Threshold)
    _max = max(Threshold)

    #group 1 : < _min
    g1 = '<' + str(Threshold[0])
    newdf.loc[newdf[NumericColumnName] < Threshold[0], NumericColumnName+' Group'] = g1

    #in the middle grouping
    if _bin > 1:
        i = _bin-1
        for x in range(i):
            bottom = x
            top = x+1
            group = str(Threshold[bottom]) +'-'+ str(Threshold[top])
            newdf.loc[newdf[NumericColumnName] >= Threshold[bottom] , NumericColumnName+' Group'] = group
    
    #group last : >= _max
    glast = '>=' + str(Threshold[_bin-1])
    newdf.loc[newdf[NumericColumnName] >= Threshold[_bin-1], NumericColumnName+' Group'] = glast
    
    DataFrame[NumericColumnName] = newdf[NumericColumnName+' Group']
    return(DataFrame)
