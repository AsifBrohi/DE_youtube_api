import pandas as pd 
def turn_dict_raw_df(dict:dict)->pd.DataFrame:
    try:
        df=pd.DataFrame.from_dict(dict["raw_df"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")
        
def turn_dict_dim_video_id(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["dim_video_id"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")

def turn_dict_dim_channel_title(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["dim_channel_title"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")

def turn_dict_dim_title(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["dim_title"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")

def turn_dict_timestamp(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["dim_timestamp"])
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
                
        df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d').dt.strftime('%Y/%m/%d')
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")

def turn_dict_duration(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["dim_duration"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")

def turn_dict_fact(dict:dict)->pd.DataFrame:
    try:
        df = pd.DataFrame.from_dict(dict["fact_table"])
        return df
    except pd.DataFrame.empty as empty_error:
        print(empty_error)
        print("DataFrame is empty")