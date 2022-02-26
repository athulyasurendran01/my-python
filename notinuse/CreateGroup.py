#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#making the group based on specified group name
#sample usage ==> NewDFwithGroup(df, 'Age', [30,20,50,30,60,40,40], ['Children','Young','Productive','Mature','Old','Senior'])
def Init(DataFrame, NumericColumnName, Threshold, BusinessName):
    
    #get the specified columnname from the DataFrame
    newdf = DataFrame[[NumericColumnName]]
    
    #remove the threshold duplicate value
    Threshold = sorted(list(dict.fromkeys(Threshold)))

    #get the threshold length, min and max value
    _bin = len(Threshold)
    _min = min(Threshold)
    _max = max(Threshold)
    
    #group 1 : < _min
    newdf.loc[newdf[NumericColumnName] < Threshold[0], NumericColumnName+' Group'] = BusinessName[0]

    #in the middle grouping
    if _bin > 1:
        i = _bin-1
        for x in range(i):
            bottom = x
            top = x+1
            group = BusinessName[top]
            newdf.loc[newdf[NumericColumnName] >= Threshold[bottom] , NumericColumnName+' Group'] = group
    
    #group last : >= _max
    newdf.loc[newdf[NumericColumnName] >= Threshold[_bin-1], NumericColumnName+' Group'] = BusinessName[_bin]

    return(newdf)  

