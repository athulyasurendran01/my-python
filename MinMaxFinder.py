#!/usr/bin/env python
# coding: utf-8

def minmaxfinder(DataFrame, NumericColumnName):
    #get the specified columnname from the DataFrame
    newdf = DataFrame[NumericColumnName]
    _min = newdf.min()
    _max = newdf.max()
    return([_min, _max])