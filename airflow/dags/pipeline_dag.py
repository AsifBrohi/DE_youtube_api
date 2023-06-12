from airflow import DAG
from airflow.operators.python import PythonOperator
from googleapiclient.discovery import build
from helpers import api_key
from helpers import api_service_name
from helpers import api_version
from helpers import playlist_id
from helpers import extract_youtube_api
from datetime import datetime

from helpers_transform import transform_data
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="extract_youtube_data",
    schedule_interval="@daily",
    start_date=datetime(2023, 6, 12)
) as dag:
    youtube = build(api_service_name, api_version, developerKey=api_key)
    download_youtube_api = PythonOperator(
        task_id="extract_youtube_API_data",
        python_callable=extract_youtube_api,
        op_kwargs={
            "youtube": youtube,
            "playlist_id": playlist_id
        }
    )
    transform_youtube_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        op_kwargs={
            'df': download_youtube_api.output
        }
    )

download_youtube_api >> transform_youtube_data
