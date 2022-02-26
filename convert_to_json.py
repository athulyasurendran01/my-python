#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import json

def json_treemap(dataframe, ls_target, ls_selected):

    ls_colname = ls_target + ls_selected
    
    if(len(ls_colname)>1):

        addcol = dataframe.drop(ls_colname, axis=1).columns.tolist()[0]
        ls_colname.append(addcol) 

        df_temp = dataframe.loc[:, ls_colname]
        grouped = df_temp.groupby(ls_colname[:-1]).count()

        levels = len(grouped.index.levels)
        dicts = [{} for i in range(levels)]
        last_index = None

        for index,value in grouped.itertuples():

            if not last_index:
                last_index = index

            for (ii,(i,j)) in enumerate(zip(index, last_index)):
                if not i == j:
                    ii = levels - ii -1
                    dicts[:ii] =  [{} for _ in dicts[:ii]]
                    break

            for i, key in enumerate(reversed(index)):
                dicts[i][key] = value
                value = dicts[i]

            last_index = index


        result = json.dumps(dicts[-1])        
        return result
        
    else:
        return "Select more then 1 data"

