import pandas as pd
from imblearn.over_sampling import RandomOverSampler

def handling_null(df):
    
    # POLICY NUMBER WILL BE IRRELEVANT IN PREDICTION SO DROPPING
    df=df.drop('policy_number',axis=1)
    
    # DROPPING IRRELEVANT RECORDS
    df.drop_duplicates(keep='last',inplace=True)
    
    # DROPPING THE OUTLIERs 
    df=df.drop(df[df['clm_cnt']>6].index)

    # FILLING NA VALUES OF VEHICLE_SUBTYPE WITH THE MODE OF THAT VEHICLE_MAKE
    df['vehicle_subtype']=df.groupby('vehicle_make')['vehicle_subtype'].transform(lambda x:x.fillna(x.mode().iloc[0]))
    
    # ASSUMING NAN CLAIM COUNT MEANING NO CLAIM HASNT BEEN TAKEN
    df['clm_cnt']=df['clm_cnt'].fillna(0)
    
    # ASSUMING NO 
    df['hypo_party']=df['hypo_party'].fillna("self")
    
    #CONSIDERING THERE WAS NO PREVIOUS INSURER AND DIGIT IS THE CUSTOMER'S FIRST INSURER
    df['prev_insurer']=df['prev_insurer'].fillna("new")
    
    df['veh_permit']=df.groupby('rto_location')['veh_permit'].transform(lambda x:x.fillna(x.mode().iloc[0]))

    return df


def sampling(df):
    X = df.drop('clm_cnt', axis=1)  
    Y = df['clm_cnt'] 
    Y.fillna(0)
    
    oversample = RandomOverSampler(sampling_strategy='auto')
    X,Y = oversample.fit_resample(X,Y)
    
    df_new = pd.concat([X, Y], axis=1)

    # Print the value counts of the target variable before and after oversampling
    
    print("\nShape PRE oversampling:")
    print(df.shape)
    
    print("\nShape POST oversampling:")
    print(df_new.shape)
    
    return df_new


def drop_testing_data(test_data):
    
    new_test_data=test_data.iloc[:,1:]
    
    return new_test_data


def handling_null_test(data):

    #data['vehicle_subtype']=data['vehicle_subtype'].fillna(df.groupby('vehicle_make')['veh_permit'].transform(lambda x:x.mode[0]))
 
    # ASSUMING NO HYPO_PARTY MEANS THAT THE VEHICLE WAS SELF FINANCED
    data['hypo_party']=data['hypo_party'].fillna("self")
    
    #CONSIDERING THERE WAS NO PREVIOUS INSURER AND DIGIT IS THE CUSTOMER'S FIRST INSURER
    data['prev_insurer']=data['prev_insurer'].fillna("new")
        
    return data

def encode_testing_data(data, count_map):
    
    # Map the values in x_test to their encoded counterparts
    x = data.copy()  # Make a copy of x_test
    
    
    for j in x.columns:
        if x[j].dtypes=='object':
            x[j]=x[j].map(count_map[j]).fillna(1)
            #need to put default values for certain columns        
            
        else:
            x[j]=x[j]
            
    
    return x