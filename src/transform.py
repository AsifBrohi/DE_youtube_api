import pandas as pd
from youtube_api import df


def transform_main():
    data_dict=transform_data(df)
    fact_table = pd.DataFrame(data_dict["fact_table"]())
    print(fact_table.head())

def transform_data(df:pd.DataFrame)->dict:
    df["publishedAt"]=pd.to_datetime(df["publishedAt"])
# creating dimension table video_id
    dim_video_id = df.drop(columns=["channelTitle","title","description",
                                    "tags","publishedAt","viewCount","likeCount",
                                    "favouriteCount","commentCount","duration",
                                    "definition","caption"])
    dim_video_id.head()

    dim_video_list = dim_video_id["video_id"].unique().tolist()
    dim_video_id = pd.DataFrame({"video_id":dim_video_list})
    dim_video_id["video_id_id"]=dim_video_id.index
    dim_video_id = dim_video_id.reindex(columns=["video_id_id","video_id"])

    # creating dimension channel title
    dim_channel_title = df.drop(columns=["video_id","title","description",
                                    "tags","publishedAt","viewCount","likeCount",
                                    "favouriteCount","commentCount","duration",
                                    "definition","caption"])
    dim_channel_title_list = dim_channel_title["channelTitle"].unique().tolist()
    dim_channel_title = pd.DataFrame({"channelTitle":dim_channel_title_list})
    dim_channel_title["channel_title_id"]=dim_channel_title.index
    dim_channel_title= dim_channel_title.reindex(columns=["channel_title_id","channelTitle"])

    # creating dimension title 
    dim_title = df.drop(columns=["video_id","channelTitle","description",
                                    "tags","publishedAt","viewCount","likeCount",
                                    "favouriteCount","commentCount","duration",
                                    "definition","caption"])
    dim_title_list = dim_title["title"].unique().tolist()
    dim_title = pd.DataFrame({"title":dim_title_list})
    dim_title["title_id"]=dim_title.index
    dim_title=dim_title.reindex(columns=["title_id","title"])

    # creating timestamp dimension 
    dim_timestamp = df.drop(columns=["video_id","title","channelTitle","description",
                                    "tags","viewCount","likeCount",
                                    "favouriteCount","commentCount","duration",
                                    "definition","caption"])
    dim_timestamp["year"]=dim_timestamp["publishedAt"].dt.year
    dim_timestamp["day"]=dim_timestamp["publishedAt"].dt.day
    dim_timestamp["week"]=dim_timestamp["publishedAt"].dt.day_of_week
    dim_timestamp["time"]=dim_timestamp["publishedAt"].dt.time
    dim_timestamp["publishedAt_id"] = dim_timestamp.index
    dim_timestamp=dim_timestamp.reindex(columns=["publishedAt_id","publishedAt",
                                                 "year","day","week","time"])
    

    # creating dimenstion duration table 
    dim_duration = df.drop(columns=["video_id","title","channelTitle","description",
                                    "tags","publishedAt","viewCount","likeCount",
                                    "favouriteCount","commentCount",
                                    "definition","caption"])
    dim_duration_list = dim_duration["duration"].unique().tolist()
    dim_duration = pd.DataFrame({"duration":dim_duration_list})
    dim_duration
    dim_duration['duration'].fillna('PT0M0S', inplace=True)

    #Extract minutes and seconds
    dim_duration[['minutes', 'seconds']] = dim_duration['duration'].str.extract(r'PT(\d+)M(\d+)S', expand=True).fillna(0).astype(int)

    #Calculate total seconds
    dim_duration['total_seconds'] = 60 * dim_duration['minutes'] + dim_duration['seconds']
    dim_duration["duration_id"]=dim_duration.index
    dim_duration = dim_duration.reindex(columns=["duration_id","duration","minutes","seconds","total_seconds"])

    fact_table = df.merge(dim_video_id,on="video_id") \
            .merge(dim_channel_title,on="channelTitle") \
            .merge(dim_title,on="title") \
            .merge(dim_timestamp,on="publishedAt") \
            .merge(dim_duration,on="duration") \
            [["video_id_id","channel_title_id","publishedAt_id","duration_id",
              "viewCount","likeCount","commentCount"
              ]]                     
                      

    return {"dim_video_id":dim_video_id.to_dict,
            "dim_channel_title":dim_channel_title.to_dict,
            "dim_title":dim_title.to_dict,
            "dim_timestamp":dim_timestamp.to_dict,
            "dim_duration":dim_duration.to_dict,
            "fact_table":fact_table.to_dict
            
            }

if __name__=="__main__":
    transform_main()

