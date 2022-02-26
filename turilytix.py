# Auther : KP Bhat
# Description : Landing page for DS Server API
import pandas as pd

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

import CategoryReplace
import DataTypeAnalyzer # Function to get col names
from DFPipe import DataFramePipe
import FeatureRank # Generates Rank
from GroupCreator import FC_CreateGroup
import ImputeCategorical # Generates Rank
import InsightGeneration # Common functions like min max, create group, insight generation
from MinMaxFinder import minmaxfinder
import Utils # Common functions

app = Flask(__name__)
api = Api(app)
CORS(app)

class DataAnalyzer(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('filePath', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        if args['filePath']:
            csvdata = pd.read_csv(args['filePath'])  # read local CSV
            global DFManager
            DFManager = DataFramePipe()
            DFManager.InsertingDataFrame(csvdata)            
            response_data = DataTypeAnalyzer.column_stats(DFManager.ReadingData()) # call external function
            data = Utils.convertToJSON(response_data)
            return {'data': data}, 200  # return data and 200 OK
        else:
            return {
                'message': "File path parameter doesn't exits"
            }, 409

class GetMinMax(Resource):
    def post(self):
        print("CreateGroup:POST")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('colName', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        data = minmaxfinder(DFManager.ReadingData(), args['colName'])
        return {'min': data[0],'max':data[1]}, 200  # return data and 200 OK

class CreateGroup(Resource):
    def post(self):
        print("CreateGroup:POST")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('colName', required=True)  # add args
        parser.add_argument('threshold')  # add args
        parser.add_argument('groupName')  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        thList = args['threshold'].split(",")
        thList =[int(x) for x in thList]
        grpList = args['groupName'].split(",")
        print("Input:",args['colName'],thList,grpList)
        DFManager.Updating(FC_CreateGroup(DFManager.ReadingData(), args['colName'],thList,grpList))
        return {'data': "OK"}, 200  # return data and 200 OK

class CategoricalImpute(Resource):
    def post(self):
        print("CategoricalImpute:POST")
        parser = reqparse.RequestParser()  # initialize
        # parser.add_argument('projectName', required=True)  # add args
        parser.add_argument('target', required=True)  # add args
        parser.add_argument('colName', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        colNames = args['colName'].split(",")
        target = args['target']
        print("input:df+", target,colNames)
        DFManager.Updating(ImputeCategorical.ImputeCategorical(DFManager.ReadingData(), target,colNames))
        return {'data': "OK"}, 200  # return data and 200 OK

class GeneratorRank(Resource):
    def post(self):
        print("GeneratorRank:POST")
        parser = reqparse.RequestParser()  # initialize
        # parser.add_argument('projectName', required=True)  # add args
        parser.add_argument('target', required=True)  # add args
        parser.add_argument('colName', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        colNames = args['colName'].split(",")
        target = args['target'].split(",")
        print("input:",target,colNames)
        rank = FeatureRank.FeatureRank(DFManager.ReadingData(),target,colNames)
        data = Utils.convertToJSON(rank)
        print("output:",data)
        return {'data': data}, 200  # return data and 200 OK

class GetCategory(Resource):
    def post(self):
        print("GetCategory:POST")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('colName', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        colName = args['colName']
        print("input:",colName)
        colList = CategoryReplace.get_value(DFManager.ReadingData(),colName)
        data = Utils.convertNumpyToArrayJSON(colList)
        print("output:",data)
        return data, 200  # return data and 200 OK

class UpdateCategory(Resource):
    def post(self):
        print("UpdateCategory:POST")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('colName', required=True)  # add args
        parser.add_argument('newValue', required=True)  # add args
        parser.add_argument('catogeries', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        colName = args['colName']
        ls_replace =args['newValue']
        ls_value = args['catogeries'].split(",")
        print("input:",colName,ls_value,ls_replace)
        DFManager.Updating(CategoryReplace.replace_value(DFManager.ReadingData(),colName,ls_value,ls_replace))
        colList = CategoryReplace.get_value(DFManager.ReadingData(),colName)
        data = Utils.convertNumpyToArrayJSON(colList)
        print("output:",data)
        return data, 200  # return data and 200 OK

class InsightGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        # parser.add_argument('filePath', required=True)  # add args
        # parser.add_argument('colName', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        # global projectDF
        # tools = InsightGeneration.InsightGeneration()
        # tools.InsertingDataFrame(projectDF)

        csvdata = pd.read_csv('./Sampel_data_churn.csv')  # read local CSV
        data = Utils.convertToJSON(csvdata)
        return {'data': data}, 200  # return data and 200 OK

# Define API
api.add_resource(DataAnalyzer, '/datatype') # add endpoint
api.add_resource(GetMinMax, '/minmax') # add endpoint
api.add_resource(CreateGroup, '/creategroup') # add endpoint
api.add_resource(CategoricalImpute, '/impute') # add endpoint
api.add_resource(GeneratorRank, '/rank') # add endpoint
api.add_resource(GetCategory, '/getcategory') # add endpoint
api.add_resource(UpdateCategory, '/updatecategory') # add endpoint
api.add_resource(InsightGenerator, '/insight') # add endpoint

# Init Server
if __name__ == '__main__':
    app.run(debug=True, port=3003)  # run our Flask app

#####################################Reference#############################################
# class Users(Resource):
#     def get(self):
#         data = pd.read_csv('users.csv')  # read local CSV
#         data = data.to_dict()  # convert dataframe to dict
#         return {'data': data}, 200  # return data and 200 OK

#     def post(self):
#         parser = reqparse.RequestParser()  # initialize
#         parser.add_argument('userId', required=True)  # add args
#         parser.add_argument('name', required=True)
#         parser.add_argument('city', required=True)
#         args = parser.parse_args()  # parse arguments to dictionary

#         # read our CSV
#         data = pd.read_csv('users.csv')

#         if args['userId'] in list(data['userId']):
#             return {
#                 'message': f"'{args['userId']}' already exists."
#             }, 409
#         else:
#             # create new dataframe containing new values
#             new_data = pd.DataFrame({
#                 'userId': [args['userId']],
#                 'name': [args['name']],
#                 'city': [args['city']],
#                 'locations': [[]]
#             })
#             # add the newly provided values
#             data = data.append(new_data, ignore_index=True)
#             data.to_csv('users.csv', index=False)  # save back to CSV
#             return {'data': data.to_dict()}, 200  # return data with 200 OK

#     def put(self):
#         parser = reqparse.RequestParser()  # initialize
#         parser.add_argument('userId', required=True)  # add args
#         parser.add_argument('location', required=True)
#         args = parser.parse_args()  # parse arguments to dictionary

#         # read our CSV
#         data = pd.read_csv('users.csv')
        
#         if args['userId'] in list(data['userId']):
#             # evaluate strings of lists to lists !!! never put something like this in prod
#             data['locations'] = data['locations'].apply(
#                 lambda x: ast.literal_eval(x)
#             )
#             # select our user
#             user_data = data[data['userId'] == args['userId']]

#             # update user's locations
#             user_data['locations'] = user_data['locations'].values[0] \
#                 .append(args['location'])
            
#             # save back to CSV
#             data.to_csv('users.csv', index=False)
#             # return data and 200 OK
#             return {'data': data.to_dict()}, 200

#         else:
#             # otherwise the userId does not exist
#             return {
#                 'message': f"'{args['userId']}' user not found."
#             }, 404

#     def delete(self):
#         parser = reqparse.RequestParser()  # initialize
#         parser.add_argument('userId', required=True)  # add userId arg
#         args = parser.parse_args()  # parse arguments to dictionary
        
#         # read our CSV
#         data = pd.read_csv('users.csv')
        
#         if args['userId'] in list(data['userId']):
#             # remove data entry matching given userId
#             data = data[data['userId'] != args['userId']]
            
#             # save back to CSV
#             data.to_csv('users.csv', index=False)
#             # return data and 200 OK
#             return {'data': data.to_dict()}, 200
#         else:
#             # otherwise we return 404 because userId does not exist
#             return {
#                 'message': f"'{args['userId']}' user not found."
#             }, 404

                    
# class Locations(Resource):
#     def get(self):
#         data = pd.read_csv('locations.csv')  # read local CSV
#         return {'data': data.to_dict()}, 200  # return data dict and 200 OK
    
#     def post(self):
#         parser = reqparse.RequestParser()  # initialize parser
#         parser.add_argument('locationId', required=True, type=int)  # add args
#         parser.add_argument('name', required=True)
#         parser.add_argument('rating', required=True)
#         args = parser.parse_args()  # parse arguments to dictionary
        
#         # read our CSV
#         data = pd.read_csv('locations.csv')
    
#         # check if location already exists
#         if args['locationId'] in list(data['locationId']):
#             # if locationId already exists, return 401 unauthorized
#             return {
#                 'message': f"'{args['locationId']}' already exists."
#             }, 409
#         else:
#             # otherwise, we can add the new location record
#             # create new dataframe containing new values
#             new_data = pd.DataFrame({
#                 'locationId': [args['locationId']],
#                 'name': [args['name']],
#                 'rating': [args['rating']]
#             })
#             # add the newly provided values
#             data = data.append(new_data, ignore_index=True)
#             data.to_csv('locations.csv', index=False)  # save back to CSV
#             return {'data': data.to_dict()}, 200  # return data with 200 OK
    
#     def patch(self):
#         parser = reqparse.RequestParser()  # initialize parser
#         parser.add_argument('locationId', required=True, type=int)  # add args
#         parser.add_argument('name', store_missing=False)  # name/rating are optional
#         parser.add_argument('rating', store_missing=False)
#         args = parser.parse_args()  # parse arguments to dictionary
        
#         # read our CSV
#         data = pd.read_csv('locations.csv')
        
#         # check that the location exists
#         if args['locationId'] in list(data['locationId']):
#             # if it exists, we can update it, first we get user row
#             user_data = data[data['locationId'] == args['locationId']]
            
#             # if name has been provided, we update name
#             if 'name' in args:
#                 user_data['name'] = args['name']
#             # if rating has been provided, we update rating
#             if 'rating' in args:
#                 user_data['rating'] = args['rating']
            
#             # update data
#             data[data['locationId'] == args['locationId']] = user_data
#             # now save updated data
#             data.to_csv('locations.csv', index=False)
#             # return data and 200 OK
#             return {'data': data.to_dict()}, 200
        
#         else:
#             # otherwise we return 404 not found
#             return {
#                 'message': f"'{args['locationId']}' location does not exist."
#             }, 404
    
#     def delete(self):
#         parser = reqparse.RequestParser()  # initialize parser
#         parser.add_argument('locationId', required=True, type=int)  # add locationId arg
#         args = parser.parse_args()  # parse arguments to dictionary

#         # read our CSV
#         data = pd.read_csv('locations.csv')
        
#         # check that the locationId exists
#         if args['locationId'] in list(data['locationId']):
#             # if it exists, we delete it
#             data = data[data['locationId'] != args['locationId']]
#             # save the data
#             data.to_csv('locations.csv', index=False)
#             # return data and 200 OK
#             return {'data': data.to_dict()}, 200
        
#         else:
#             # otherwise we return 404 not found
#             return {
#                 'message': f"'{args['locationId']}' location does not exist."
#             }