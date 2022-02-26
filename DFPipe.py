#!/usr/bin/env python
# coding: utf-8

import pandas as pd

class DataFramePipe:

    OriginalDataFrame = None
    UpdatedDataFrame = None
    LastCopyDataFrame = None
    
    def __init__(self):
        pass

    @classmethod
    def InsertingDataFrame(cls, Data):
        DataFramePipe.OriginalDataFrame = Data
        pass

    @classmethod
    def ResetDataFrame(cls):
        DataFramePipe.OriginalDataFrame = None
        DataFramePipe.UpdatedDataFrame = None

    @classmethod
    def LastCopyDataFrameCM(cls):
        DataFramePipe.UpdatedDataFrame = DataFramePipe.LastCopyDataFrame
    
    def ReadingData(self):

        OutputDataFrame = None

        while OutputDataFrame == None:
            
            if DataFramePipe.UpdatedDataFrame is not None:
                OutputDataFrame = DataFramePipe.UpdatedDataFrame.copy(deep=False)
                break
            
            if DataFramePipe.OriginalDataFrame is not None:
                OutputDataFrame = DataFramePipe.OriginalDataFrame.copy(deep=False)
                break
            
            if DataFramePipe.UpdatedDataFrame is None and DataFramePipe.OriginalDataFrame is None:
                print('Datafame not ready')
                break

        return OutputDataFrame 

    def Updating(self, Out):
        if isinstance(Out, pd.DataFrame) == True:

            if DataFramePipe.UpdatedDataFrame is not None:
                DataFramePipe.LastCopyDataFrame = DataFramePipe.UpdatedDataFrame
            if DataFramePipe.UpdatedDataFrame is None:
                DataFramePipe.LastCopyDataFrame = DataFramePipe.OriginalDataFrame
                                
            DataFramePipe.UpdatedDataFrame = Out
            return self.ReadingData()
        else:
            return Out    
