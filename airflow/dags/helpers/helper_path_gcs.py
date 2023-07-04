from google.cloud import storage 

GCP_PROJECT_ID='youtube-api-388114'
GCP_GCS_BUCKET='de_youtube_api'
def get_gcs_object_path(project_id:str,bucket_name:str,object_name:str):
    '''Returns url for object in GCS bucket
    :param:project_id:str - project_id code
    :param:bucket_name:str - GCS bucket name
    :param:object_name:str - object you want to use inside the GCS bucket
    :return:URL- returns url of the object inside GCS bucekt

    This function takes in parameters above and returns url of the object
    inside the GCS bucket
    
    '''

    client = storage.Client(project=project_id)

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.public_url

path_of_gcs_object = get_gcs_object_path(GCP_PROJECT_ID,GCP_GCS_BUCKET,"raw_youtube_data.csv")
