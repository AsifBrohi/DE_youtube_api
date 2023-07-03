from googleapiclient.discovery import build
import pandas as pd
import os
import re
api_key = "your_api_key"
api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client

youtube = build(
api_service_name, api_version, developerKey=api_key)

playlist_id = "playlist_id"
def extract_youtube_api(youtube:str, playlist_id:str):
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
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']
            

            for key in stats_to_keep.keys():
                for value in stats_to_keep[key]:
                    try:
                    # Remove special characters and emojis from description and tags
                        if value in ['title', 'tags']:
                            cleaned_text = re.sub(r'[^\w\s]', '', video[key][value])
                            video_info[value] = cleaned_text
                        else:
                            video_info[value] = video[key][value]
                    except:
                        video_info[value] = None
            all_video_info.append(video_info)
    
    df = pd.DataFrame(all_video_info)
    
    return df.to_csv("raw_youtube_data.csv")
    
extract_youtube_api(youtube,playlist_id)


