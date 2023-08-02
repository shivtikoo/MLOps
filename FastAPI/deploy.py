from fastapi import FastAPI,File, Form, UploadFile
from pydantic import BaseModel
import pandas as pd
from io import StringIO
import requests
from PreProcessing import handling_null
from PreProcessing import handling_null_test
from PreProcessing import drop_testing_data
from PreProcessing import encode_testing_data
import numpy as np

# 2. Create the app object
app = FastAPI()

class Claim_Count(BaseModel):
    policy_number:    str
    office_code:      int
    policy_period:    int
    imd_code:         int
    imd_channel:      str
    vehicle_make:     str
    vehicle_model:    str
    vehicle_subtype:  str
    fuel_type:        str
    rto_location:     str
    veh_permit:       str
    veh_age:          int
    prev_insurer:     str
    prev_ncb:         int
    policy_type:      str
    net_premium:      int
    sum_insured:      int
    hypo_party:       str

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')

def index():
        return {'message': 'PREDICT THE NO. OF CLAIMS'}


# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')

def online_prediction(data:Claim_Count):

    data = data.dict()

    # preprocessing on the original dataset
    df= pd.read_csv('C:/Users/Shiv.tikoo/Downloads/Project/Data/auto policies.csv')
    df = handling_null(df)
    
    count_map={}
    
    for x in df.columns:
        if df[x].dtypes=="object":
            count_map[x]=dict(df[x].value_counts())
 
        else:
            continue

    index=[ "policy_number","office_code","policy_period","imd_code","imd_channel","vehicle_make",
    "vehicle_model","vehicle_subtype","fuel_type","rto_location","veh_permit",'veh_age',"prev_insurer",
    "prev_ncb","policy_type","net_premium","sum_insured","hypo_party"]


    
    data=pd.DataFrame(data,index=index)
    data=drop_testing_data(data)
    data=handling_null_test(data,df)
    data=encode_testing_data(data,count_map)

    data_in = data.values.tolist()

    endpoint="http://localhost:1568/invocations"

    inference_request={
        "dataframe_records":data_in
    }

    response= requests.post(endpoint, json=inference_request)

    return {
        'CLAIM COUNT Prediction': response.text,
    }






        

    


