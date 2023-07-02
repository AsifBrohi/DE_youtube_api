import pandas_gbq
def load_raw_df(df,table_id)->None:
    pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_video_id(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_channel_title(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_title(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_timestamp(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_dim_duration(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")

def load_fact(df,table_id)->None:
     pandas_gbq.to_gbq(df,table_id,if_exists="replace")