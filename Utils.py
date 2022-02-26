#!/usr/bin/env python
# coding: utf-8
# Auther : KP Bhat
# Description : Reusable functions

import pandas as pd
import numpy
import json
from json import JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def convertToJSON(df):
    result = df.to_json(orient='records')
    resultJSON = json.loads(result)
    return resultJSON

def convertNumpyToArrayJSON(list):
    numpyData = {"data": list}
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
    decodedArrays = json.loads(encodedNumpyData)
    # finalNumpyArray = numpy.asarray(decodedArrays["array"])
    # print("NumPy Array")
    # print(finalNumpyArray)
    return decodedArrays

def saveDF(df):
    result = df.to_json(orient='records')
    resultJSON = json.loads(result)
    return resultJSON
