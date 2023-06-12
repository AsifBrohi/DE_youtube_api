from googleapiclient.discovery import build
import pandas as pd

api_key = "AIzaSyB6K1dPTHKB3e0bfAKoaAeU6BY3rEXcFo0"
api_service_name = "youtube"
api_version = "v3"
# channel_id="UCNAf1k0yIjyGu3k9BwAg3lg"
channel_id="UCDvErgK0j5ur3aLgn6U-LqQ"
# Get credentials and create an API client

youtube = build(
api_service_name, api_version, developerKey=api_key)
playlist_id = "UUChmJrVa8kDg05JfCmxpLRw"
def extract_youtube_api(youtube:str, playlist_id:str)->pd.DataFrame:
    data = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for video in response["items"]:
            data.append(video["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break
    all_video_info = []
    
    for info in range(0, len(data), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=data[info:info+50]
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']
            

            for key in stats_to_keep.keys():
                for value in stats_to_keep[key]:
                    try:
                        video_info[value] = video[key][value]
                    except:
                        video_info[value] = None

            all_video_info.append(video_info)
    
    df=pd.DataFrame(all_video_info)
    return df


