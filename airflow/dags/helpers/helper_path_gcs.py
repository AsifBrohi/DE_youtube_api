from google.cloud import storage 

GCP_PROJECT_ID='youtube-api-388114'
GCP_GCS_BUCKET='de_youtube_api'
def get_gcs_object_path(project_id:str,bucket_name:str,object_name:str):

    client = storage.Client(project=project_id)

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.public_url

path_of_gcs_object = get_gcs_object_path(GCP_PROJECT_ID,GCP_GCS_BUCKET,"raw_youtube_data.csv")
