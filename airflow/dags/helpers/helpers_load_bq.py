import pandas_gbq
def load_raw_df(df,table_id)->None:
    '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''
    pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_video_id(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''

     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_channel_title(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_title(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_timestamp(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''    
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_duration(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''    
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_fact(df,table_id)->None:
     '''
    :param:df:pd.Dataframe - Dataframe
    :param:table_id:str - Table_id inside bigquery
    :returns:None

    This function takes two parameters and loads data 
    into a certain table in bigquery
    
    '''    
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")