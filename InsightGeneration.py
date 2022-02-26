# %%
# %%
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

import json
import math
from googletrans import Translator
import warnings
warnings.filterwarnings("ignore")
from convert_to_json import json_treemap


''''
How to call Sunburst/Treemap:
ls_target = ['AdminFee'] --> this is target variable
ls_selected = ['ShoppingReward', 'RestaurantReward', 'BigOutlet'] --> this is selected variable

IG = InsightGeneration()
IG.InsertingDataFrame(LatestDF)
Wording, Data = IG.TreeMapChart(ls_target, ls_selected)

Wording: This is wording insight already in JSON
Data: Pivot data already in JSON format
'''

# %%
class InsightGeneration:

    DataFrame = None
    UpdatedFrame = None

    def __init__(self, DataDir=None, TargetLanguage=None):

        self.DataDir = DataDir
        self.TargetLanguage = TargetLanguage

    @classmethod
    def InsertingDataFrame(cls, DataFrame):
        cls.DataFrame = DataFrame        

    @classmethod
    def UpdatingDataFrame(cls, DataFrame):
        cls.UpdatedFrame = DataFrame

    @classmethod
    def ResetModifiedDataFrame(cls):
        cls.UpdatedFrame = None

    # This will round up the values
    def Flooring(self, input):
    
        return round(input, 3)        

    # This will Translate the teks, the argument is user input
    def Translate(self, Teks):

        Translator_ = Translator(service_urls=['translate.googleapis.com'])
        Translation = Translator_.translate(Teks, dest=self.TargetLanguage)

        return Translation.text

    # This will read csv data in certain Directory
    def ReadingData(self):
        '''
        1. Check modified df, if exist will return into it
        2. Check originial df, if exist will reurn into it
        3. If both fail, will read df
        This will consume less memory
        '''

        OutputDataFrame = None

        while OutputDataFrame == None:
            
            if InsightGeneration.UpdatedFrame is not None:
                OutputDataFrame = InsightGeneration.UpdatedFrame
                break
            
            if InsightGeneration.DataFrame is not None:
                OutputDataFrame = InsightGeneration.DataFrame
                break

            if InsightGeneration.DataFrame is None and InsightGeneration.UpdatedFrame is None:
                print('Dataframe is not ready')
                break
            
        return OutputDataFrame

    # This will loc dataframe based on certain columns
    def GeneratingItem(self, Col):

        DataPartition = self.ReadingData()[Col]

        return DataPartition

    # This will Describing the 1 columns partition by GeneratingItem methods
    def Describing(self, Col):
        
        return self.GeneratingItem(Col).describe()

    # This will identifying certain columns names data type
    def DtypeIdentification(self, Col):
    
        return self.ReadingData()[Col].dtype

    # This will generate unique item in first col in Target variable
    def UniqueItemInCertainColumns(self, ls1):
        return self.ReadingData()[ls1[0]].unique().tolist()

    # This will getting statistics item based on data type columns by DtypeIdentification methods
    def GettingItem(self, Col):

        dtype = 0

        if self.DtypeIdentification(Col) == 'int64':

            dtype = 'Numerical'

            count = self.Describing(Col)[0]
            mean = self.Describing(Col)[1]
            min = self.Describing(Col)[3]
            max = self.Describing(Col)[7]

            return dtype, self.Flooring(count), self.Flooring(mean), self.Flooring(min), self.Flooring(max)

        if self.DtypeIdentification(Col) == 'O':

            dtype = 'Categorical'

            count = self.Describing(Col)[0]
            unique = self.Describing(Col)[1]
            top_item = self.Describing(Col)[2]
            freq = self.Describing(Col)[3]

            return dtype, self.Flooring(count), self.Flooring(unique), top_item, self.Flooring(freq)

    # This will crostab the 2 categorical columns
    def Crosstabbing(self, Col1, Col2):
            
        return pd.crosstab(self.ReadingData()[Col1], self.ReadingData()[Col2])

    # This will sort the Crosstabbing data and returns as follows
    def Sorting(self, data, sort_by):

        Sort = data.sort_values(by=sort_by, ascending=False)[sort_by]

        Highest = Sort[:1].index.item()

        HighestValues = Sort[:1].values.item()

        Mean = Sort.describe()[1:2].values.item()

        BelowMean =  Sort.loc[Sort < Mean].index.values.tolist()

        StringBelowMean = ', '.join(str(x) for x in BelowMean)

        return Highest, HighestValues, Mean, BelowMean, StringBelowMean     

    # This will combining the list for pivot
    def CombiningPivotCol(self, ls1, ls2):
        return ls1 + ls2

    def CalculateLenItemInPivot(self, ls1, ls2):
        return len(ls1+ls2)

    # This wil calculate stacking based on len of Target variable
    def CalculateStacking(self, ls2):
        if len(ls2) == 1:
            Stack = [0]
        elif len(ls2) == 2:
            Stack = [0,1]
        elif len(ls2) == 3:
            Stack = [0,0,1]
        elif len(ls2) == 4:
            Stack = [0,0,0,1]
        else:
            print('Too Many Indeks to Stack')

        return Stack

    # This will pivot table di columns (ls1, ls2). Must caution, ls1 is Target variable (must categorical), ls2 is ranked variable
    def PivotTable(self, ls1, ls2):
        return pd.pivot_table(self.ReadingData()[self.CombiningPivotCol(ls1, ls2)], 
                              index=ls1, 
                              columns=ls2,
                              aggfunc=len, 
                              fill_value=0)

    # This will return final pivotting
    def PivotStacking(self, ls1, ls2):
        df = self.PivotTable(ls1, ls2).stack(self.CalculateStacking(ls2)).reset_index(name='Count')
        df = df.sort_values(by='Count', ascending= False)
        df.reset_index(drop=True, inplace=True)
        return df

    # This will calculate average count pivotting
    def CalculateAverageCountPivot(self, DataForParse):
        return self.Flooring(DataForParse['Count'].mean())

    # This will calculate sum of count from pivotting
    def CalculatingSumCountPivot(self, DataForParse):
        return self.Flooring(DataForParse['Count'].sum())
    
    # This will generate index and values for max count in pivot as a string
    def GenerateMinStringFromPivot(self, ls1, ls2, DataForParse):
        ItemFromIndex = DataForParse.iloc[-1].index[0:self.CalculateLenItemInPivot(ls1, ls2)].tolist()
        ItemFromvalues = DataForParse.iloc[-1].values[0:self.CalculateLenItemInPivot(ls1, ls2)].tolist()
        return ' and '.join(str(x) for x in ItemFromIndex), ' and '.join(str(x) for x in ItemFromvalues)

    # This will generate index and values for min count in pivot as a string
    def GenerateMaxStringFromPivot(self, ls1, ls2, DataForParse):
        ItemFromIndex = DataForParse.iloc[0].index[0:self.CalculateLenItemInPivot(ls1, ls2)].tolist()
        ItemFromvalues = DataForParse.iloc[0].values[0:self.CalculateLenItemInPivot(ls1, ls2)].tolist()
        return ' and '.join(str(x) for x in ItemFromIndex), ' and '.join(str(x) for x in ItemFromvalues)

    # This will calculate max count after pivotting
    def CalculateMaxCountFromPivot(self, DataForParse):
        return DataForParse.iloc[0]['Count'].item()

    # This will calculate min count after pivotting
    def CalculateMinCountFromPivot(self, DataForParse):
        return DataForParse.iloc[-1]['Count'].item()

    # This will aggregate 2 colums (XAxis and YAxis) with certain method
    def CustomAggregation(self, XAxis, YAxis, Method):

        custom_aggregation = {}
        custom_aggregation[YAxis] = Method
        df = self.ReadingData().groupby(XAxis).agg(custom_aggregation)
        df.columns = [YAxis]
        df[XAxis] = df.index    
        df.reset_index(drop=True, inplace=True)
        df = df.sort_values(by=YAxis, ascending=False)
        return df

    def GetItemFromAggregation(self, DataForSearch, XAxis, YAxis, Item):

        return DataForSearch.loc[DataForSearch[XAxis] == Item][YAxis].item()

    def RoundingTo2(self, int):
        return round(int, 2)

    def GetTotalRowsFromData(self):
        return int(self.ReadingData().shape[0])

    def GetRenamedColumns(self, Columns):
        return [Columns, Columns+'_Group']

    def Jsoning(self, Dict, Item, ID):
        
        Add = {f'Insight{ID}': Item}

        return Dict.update(Add)
        

    # This will generate individual columns insight
    def FirstInsight(self, ColumnName):
    
        dtype, _ , _ , _ , _ = self.GettingItem(ColumnName)

        if dtype == 'Numerical':

            _ , Count, Mean, Min, Max = self.GettingItem(ColumnName)

        if dtype == 'Categorical':

            _ , Count, Unique, TopItem, Freq = self.GettingItem(ColumnName)

            perc = (Freq/Count) * 100

            Wording = f'In {ColumnName}, there are {Unique} categories where {TopItem} has the most contribution of {Freq} times or {self.Flooring(perc)}% from total data.'

            if self.TargetLanguage:
                
                Wording = self.Translate(Wording)
                return Wording

            else:
                
                return Wording

        if dtype == 'Numerical':

            _ , Count, Mean, Min, Max = self.GettingItem(ColumnName)

            Wording = f'{ColumnName}, have mean values {Mean}. Meanwhile for minimum value is {Min}, and max value is {Max}'

            if self.TargetLanguage:
                print(self.Translate(Wording))
            else:
                print(Wording)                

    # This will generating pairing insight based on dtype (Cat-Cat, Num-Num, Cat-Num or reverse)
    def SecondInsight(self, ColumnName1, ColumnName2):

        if self.DtypeIdentification(ColumnName1) == 'int64' and self.DtypeIdentification(ColumnName2) == 'int64':

            _ , _ , MeanCol1, MinCol1, MaxCol1 = self.GettingItem(ColumnName1)       

            _ , _ , MeanCol2, MinCol2, MaxCol2 = self.GettingItem(ColumnName2)       

            Wording1 = f'Pada kolom {ColumnName1} memiliki nilai rata-rata sebesar {MeanCol1} sedangkan untuk kolom {ColumnName2} memiliki nilai rata-rata sebesar {MeanCol2}, selisih rata-rata kedua kolom tersebut sebesar {abs(MeanCol1-MeanCol2)}'

            Wording2 = f'Pada kolom {ColumnName1} memiliki nilai minimum sebesar {MinCol1} sedangkan untuk kolom {ColumnName2} memiliki nilai minimum sebesar {MinCol2}, selisih nilai minimum kedua kolom tersebut sebesar {abs(MinCol1-MinCol2)}'

            Wording3 = f'Pada kolom {ColumnName1} memiliki nilai maksimum sebesar {MaxCol1} sedangkan untuk kolom {ColumnName2} memiliki nilai maksimum sebesar {MaxCol2}, selisih nilai maksimum kedua kolom tersebut sebesar {abs(MaxCol1-MaxCol2)}'

            if self.TargetLanguage:

                print(self.Translate(Wording1))
                print(self.Translate(Wording2))
                print(self.Translate(Wording3))

            else:
                
                print(Wording3)
                print(Wording3)
                print(Wording3)

        elif self.DtypeIdentification(ColumnName1) == 'O' and self.DtypeIdentification(ColumnName2) == 'O':

            for item in self.Crosstabbing(ColumnName1, ColumnName2).columns.tolist():
                
                highest, values, mean, below_mean, str_below_mean = self.Sorting(self.Crosstabbing(ColumnName1, ColumnName2), item)

                Wording = f'Based on item {item} in column {ColumnName2}, item {highest} in column {ColumnName1} have highest value {values} with average is {self.Flooring(mean)}. There is {len(below_mean)} item that below the average, which is {str_below_mean}'

                if self.TargetLanguage:

                    print(self.Translate(Wording))

                else:
                    print(Wording)
        else:
            print('Not thinking about it yet...')
            
    # This for sunburst insight
    def TreeMapChart(self, ls1, ls2):

        Dict = {}
        self.Jsoning(Dict, self.FirstInsight(ls1[0]), 0)

        Count = -1
        for i in ls2:
            
            Count += 2

            ItemIter = []
            ItemIter.append(i)

            Pivot = self.PivotStacking(ls1, ItemIter)

            _ , MinValues = self.GenerateMinStringFromPivot(ls1, ItemIter, Pivot)

            MaxIndex, MaxValues = self.GenerateMaxStringFromPivot(ls1, ItemIter, Pivot)

            MaxCountPercentages = self.Flooring((self.CalculateMaxCountFromPivot(Pivot) / self.CalculatingSumCountPivot(Pivot)) * 100)

            MinCountPercentages = self.Flooring((self.CalculateMinCountFromPivot(Pivot) / self.CalculatingSumCountPivot(Pivot)) * 100)

            MaxAppears = self.Flooring(self.CalculateMaxCountFromPivot(Pivot))

            Wording1 = f'For {MaxIndex} with combination of {MaxValues} has highest contribution of {MaxAppears} times or {MaxCountPercentages}% from total data. Meanwhile combination of {MinValues} has the lowest contribution of {MinCountPercentages}% from total data.'

            if self.TargetLanguage:
                self.Jsoning(Dict, self.FirstInsight(i), Count)
                self.Jsoning(Dict, Wording1, Count+1)                
            
            else:
                self.Jsoning(Dict, self.FirstInsight(i), Count)
                self.Jsoning(Dict, Wording1, Count + 1)          

        FinalWordJs = json.dumps(Dict, indent = 4)
        DataJs = json_treemap(self.ReadingData(), ls1, ls2)
        
        return FinalWordJs, DataJs       

    def ChartInsight(self, XAxis, YAxis, Method):

        df = self.CustomAggregation(XAxis, YAxis, Method)
        count = self.CustomAggregation(XAxis, YAxis, 'count')
        min = self.CustomAggregation(XAxis, YAxis, 'min')
        max = self.CustomAggregation(XAxis, YAxis, 'max')

        XAxisItem = df[XAxis].tolist()
        Highest = XAxisItem[0]
        Lowest = XAxisItem[-1]

        HighestMethodValue = self.Flooring(self.GetItemFromAggregation(df, XAxis, YAxis, Highest))
        LowestMethodValue = self.Flooring(self.GetItemFromAggregation(df, XAxis, YAxis, Lowest))

        HighestCountValueForHighest = self.Flooring(self.GetItemFromAggregation(count, XAxis, YAxis, Highest))
        HighestCountPercentagesForHighest = self.RoundingTo2((self.GetItemFromAggregation(count, XAxis, YAxis, Highest)) / self.GetTotalRowsFromData()) * 100
        MinimumValueForHighest = self.GetItemFromAggregation(min, XAxis, YAxis, Highest)
        MaximumvalueForHighest = self.GetItemFromAggregation(max, XAxis, YAxis, Highest)

        HighestCountValueForLowest = self.Flooring(self.GetItemFromAggregation(count, XAxis, YAxis, Lowest))
        HighestCountPercentagesForLowest = self.RoundingTo2((self.GetItemFromAggregation(count, XAxis, YAxis, Lowest)) / self.GetTotalRowsFromData()) * 100
        MinimumValueForLowest = self.GetItemFromAggregation(min, XAxis, YAxis, Lowest)
        MaximumValueForLowest = self.GetItemFromAggregation(max, XAxis, YAxis, Lowest)

        Wording1 = f'{Highest} in {XAxis} have highest {Method} value of {YAxis} which is {HighestMethodValue}. Meanwhile {Lowest} have lowest values which is {LowestMethodValue}'

        Wording2 = f'{Highest} in {XAxis} appears {HighestCountValueForHighest} times in this data or {HighestCountPercentagesForHighest} % from total data. Minimum values of {XAxis} that {Highest} have is {MinimumValueForHighest}. Meanwhile for the maximum values is {MaximumvalueForHighest}.'

        Wording3 = f'{Lowest} in {XAxis} appears {HighestCountValueForLowest} times in this data or {HighestCountPercentagesForLowest} % from total data. Minimum values of {XAxis} that {Lowest} have is {MinimumValueForLowest}. Meanwhile for the maximum values is {MaximumValueForLowest}.'    

        Dict = {}
        
        if self.TargetLanguage:

            self.Jsoning(Dict, self.Translate(Wording1), 0)        
            self.Jsoning(Dict, self.Translate(Wording2), 1)        
            self.Jsoning(Dict, self.Translate(Wording3), 2)        

        else:
            self.Jsoning(Dict, Wording1, 0)
            self.Jsoning(Dict, Wording2, 1)
            self.Jsoning(Dict, Wording3, 2)

        return json.dumps(Dict, indent = 4) 

IG = InsightGeneration()
# %%

# %%
# ls_target = ['AdminFee']
# ls_selected = ['ShoppingReward', 'RestaurantReward', 'BigOutlet']

# Wording, Data = IG.SunBurstInsight(ls_target, ls_selected)

# %%



