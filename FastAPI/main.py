
# #CREATING VIRTUAL ENVIRONMENT
# #python -m venv fastapienv
# #ACTIVATING
# #go to the directory fastapienv\Scripts\activate

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import requests
from PreProcessing import handling_null_test, drop_testing_data

app = FastAPI()

class ClaimCount(BaseModel):
    # Define all the required fields here
    # Make sure the field names match the expected feature names in the model
    policy_number: str
    office_code: int
    policy_period: int
    imd_code: int
    imd_channel: str
    vehicle_make: str
    vehicle_model: str
    vehicle_subtype: str
    fuel_type: str
    rto_location: str
    veh_permit: str
    veh_age: int
    prev_insurer: str
    prev_ncb: int
    policy_type: str
    net_premium: int
    sum_insured: int
    hypo_party: str

@app.get('/')
async def root():
    return {'message': 'PREDICT IF CLAIM WILL BE TAKEN OR NOT'}

@app.post('/predict')
async def online_prediction(data: ClaimCount):
    data_dict = data.dict()

    print("INPUT:\n")
    print(data_dict,"\n")

    # Perform data processing on pandas DataFrame instead of using functions
    cols_to_drop = ['veh_permit', 'prev_ncb', 'fuel_type', 'vehicle_make', 'policy_type']
    data = pd.DataFrame(data_dict, index=[0]).drop(columns=cols_to_drop)



    #DROPPING THE POLICY NUMBER
    data = drop_testing_data(data)
    #HANDLING NULL VALUES
    data = handling_null_test(data)

    # Prepare the input data as a list of dictionaries
    data_in = data.to_dict(orient='records')

    print("INPUT:\n")
    print(data,"\n")

    endpoint = "http://localhost:1568/invocations"

    # Send the request as JSON
    response = requests.post(endpoint, json={"dataframe_records": data_in})
    predict_response = response.json()

    if "predictions" in predict_response and len(predict_response["predictions"]) > 0:
        prediction_value = predict_response["predictions"][0]
        if prediction_value == 0:
            return {'CLAIM COUNT Prediction': predict_response, 'message': 'NO CLAIM IS PREDICTED!!'}
        else:
            return {'CLAIM COUNT Prediction': predict_response, 'message': 'CLAIM IS PREDICTED!!'}
    else:
        return {'message': 'Error in the prediction response.'}
    


# from fastapi import FastAPI
# from pydantic import BaseModel
# import pandas as pd
# import requests
# import json

# from PreProcessing import handling_null, handling_null_test, drop_testing_data, encode_testing_data, sampling

# app = FastAPI()

# class ClaimCount(BaseModel):
#     policy_number: str
#     office_code: int
#     policy_period: int
#     imd_code: int
#     imd_channel: str
#     vehicle_make: str
#     vehicle_model: str
#     vehicle_subtype: str
#     fuel_type: str
#     rto_location: str
#     veh_permit: str
#     veh_age: int
#     prev_insurer: str
#     prev_ncb: int
#     policy_type: str
#     net_premium: int
#     sum_insured: int
#     hypo_party: str

# #ROOT METHOD
# @app.get('/')
# async def root():
#     return {'message': 'PREDICT IF CLAIM WILL BE TAKEN OR NOT'}


# @app.post('/predict')
# async def online_prediction(data: ClaimCount):

#     data=data.dict()
#     print("INPUT:\n")
#     print(data,"\n")

#     #STORING THE COUNT MAP
#     # df = pd.read_excel('C:/Users/Shiv.tikoo/Downloads/Project/Data/tmp_auto_poicies_202306261442.xlsx')
#     # df = handling_null(df)
#     # df = sampling(df)
#     # count_map = {}
#     # for column in df.columns:
#     #     if df[column].dtypes == "object":
#     #         count_map[column] = dict(df[column].value_counts())
 

#     #PRE PROCESSING THE TESTING DATA WITH THE HELP OF COUNT_MAP
#     # index = ["policy_number", "office_code", "policy_period", "imd_code", "imd_channel", "vehicle_make",
#     #          "vehicle_model", "vehicle_subtype", "fuel_type", "rto_location", "veh_permit", "veh_age",
#     #          "prev_insurer", "prev_ncb", "policy_type", "net_premium", "sum_insured", "hypo_party"]

#     data = pd.DataFrame(data, index=[0])
#     #DROPPING THE POLICY NUMBER
#     data = drop_testing_data(data)
#     #HANDLING NULL VALUES
#     data = handling_null_test(data)
#     #ENCODING TO FIT THE MODEL   
#     # data = encode_testing_data(data, count_map)
#     cols_to_drop=['veh_permit','prev_ncb','fuel_type','vehicle_make','policy_type']
#     data=data.drop(columns=cols_to_drop,axis=1)

    

#     #GET PREDICTIONS

#     #CONVERSION OF THE DATAFRAME TO LIST
#     data_in = data.values.tolist()

#     print("INPUT:\n")
#     print(data_in,"\n")

#     endpoint = "http://localhost:1568/invocations"


#     # inference_request = {
#     #     "dataframe_records": data_in
#     # }

#     #CONVERSION OF LIST TO JSON
#     input_json={
#         "dataframe_records":data_in
#     }
    
#     #input_json=json.dumps(input_json)
#     #print(input_json)

#     #PREDICTION
#     response = requests.post(endpoint, json=input_json)

#     predict_count=response.json()

#     return {
#         'CLAIM COUNT Prediction': predict_count,
#     }










# from fastapi import FastAPI,File, Form, UploadFile
# from pydantic import BaseModel
# import pickle
# import numpy as np
# import pandas as pd
# from io import StringIO
# import requests
# from PreProcessing import handling_null
# from PreProcessing import handling_null_test
# from PreProcessing import drop_testing_data
# from PreProcessing import encode_testing_data
# import numpy as np

# app= FastAPI()

# class Claim_Count(BaseModel):
#     policy_number:    str
#     office_code:      int
#     policy_period:    int
#     imd_code:         int
#     imd_channel:      str
#     vehicle_make:     str
#     vehicle_model:    str
#     vehicle_subtype:  str
#     fuel_type:        str
#     rto_location:     str
#     veh_permit:       str
#     veh_age:          int
#     prev_insurer:     str
#     prev_ncb:         int
#     policy_type:      str
#     net_premium:      float
#     sum_insured:      int
#     hypo_party:       str


# @app.get("/")

# async def root():
#     return {"Message":"PREDICT how many times a person will take CLAIM"}

# @app.post("/predict")

# async def Online_Prediction(x: Claim_Count):
    
#     data=x.dict()

#     # preprocessing on the original dataset
#     df= pd.read_csv('C:/Users/Shiv.tikoo/Downloads/Project/Data/auto policies.csv')
#     df = handling_null(df)
    
#     count_map={}
    
#     for x in df.columns:
#         if df[x].dtypes=="object":
#             count_map[x]=dict(df[x].value_counts())
 
#         else:
#             continue

#     index=[ "policy_number","office_code","policy_period","imd_code","imd_channel","vehicle_make",
#     "vehicle_model","vehicle_subtype","fuel_type","rto_location","veh_permit",'veh_age',"prev_insurer",
#     "prev_ncb","policy_type","net_premium","sum_insured","hypo_party"]

#     data=pd.DataFrame(data,index=index)
#     data=drop_testing_data(data)
#     data=handling_null_test(data,df)
#     data=encode_testing_data(data,count_map)

#     data_in = data.values.tolist()

#     print(data_in)
#     endpoint="http://localhost:1568/invocations"
#     inference_request={
#         "dataframe_records":data_in
#     }

#     print(inference_request)

#     response= requests.post(endpoint, json=inference_request)

#     print(response)

#     return {
#         'CLAIM COUNT Prediction': response.text,
#     }

# @app.post('/files')
# async def Batch_Prediction(data: UploadFile):

#     #s=str(file,'utf=8')
#     #data=StringIO(s)

#     #preprocessing on the original dataset
#     df= pd.read_csv('C:/Users/Shiv.tikoo/Downloads/Project/Data/auto policies.csv')
#     df = handling_null(df)
    
#     count_map={}
    
#     for x in df.columns:
#         if df[x].dtypes=="object":
#             count_map[x]=dict(df[x].value_counts())
 
#         else:
#             continue

#     index=[ "policy_number","office_code","policy_period","imd_code","imd_channel","vehicle_make",
#     "vehicle_model","vehicle_subtype","fuel_type","rto_location","veh_permit",'veh_age',"prev_insurer",
#     "prev_ncb","policy_type","net_premium","sum_insured","hypo_party"]

#     file_contents=await data.read()
#     try:
#         data=pd.read_excel(StringIO(file_contents.decode('utf-8')))
#     except UnicodeDecodeError:
#         data=pd.read_excel(StringIO(file_contents.decode('latin-1')))



#     #PreProcessing on the TestData
#     data=drop_testing_data(data)
#     data=handling_null_test(data,df)
#     data=encode_testing_data(data,count_map)

#     data_in = data.values.tolist()
#     print(data_in)
#     endpoint="http://localhost:1568/invocations"

#     inference_request={
#         "dataframe_records":data_in
#     }

#     print(inference_request)

#     response= requests.post(endpoint, json=inference_request)
#     print(response)

#     return {
#         'CLAIM COUNT Prediction': response.text,
#     }


#     # TO RUN uvicorn main2:app --reload

