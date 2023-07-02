from airflow import DAG
from airflow.operators.python import PythonOperator
from googleapiclient.discovery import build
from airflow.utils.task_group import TaskGroup
from helpers.helpers import api_key
from helpers.helpers import api_service_name
from helpers.helpers import api_version
from helpers.helpers import playlist_id
from helpers.helpers import extract_youtube_api
from datetime import datetime
from helpers.helpers_transform import transform_data
from helpers.helpers_gcs import BUCKET
from helpers.helpers_gcs import upload_to_gcs
from helpers.helper_path_gcs import path_of_gcs_object
from helpers.helpers_df import turn_dict_raw_df
from helpers.helpers_df import turn_dict_dim_video_id
from helpers.helpers_df import turn_dict_dim_channel_title
from helpers.helpers_df import turn_dict_dim_title
from helpers.helpers_df import turn_dict_timestamp
from helpers.helpers_df import turn_dict_duration
from helpers.helpers_df import turn_dict_fact
from helpers.helpers_load_bq import load_raw_df
from helpers.helpers_load_bq import load_dim_video_id
from helpers.helpers_load_bq import load_dim_channel_title
from helpers.helpers_load_bq import load_dim_title
from helpers.helpers_load_bq import load_dim_timestamp
from helpers.helpers_load_bq import load_dim_duration
from helpers.helpers_load_bq import load_fact
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

    
    write_csv_to_gcs = PythonOperator(
        task_id = "load_onto_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            
            "bucket":BUCKET,
            "object_name":"raw_youtube_data.csv",
            "file":download_youtube_api.output
        }

    )
    
    transform_youtube_data = PythonOperator(
        
        task_id="transform_data",
        python_callable=transform_data,
        op_kwargs={
            "file_path":path_of_gcs_object
        }
    )

    with TaskGroup("processing_dataframe_tasks") as process_dataframe:
        process_raw_data = PythonOperator(
            task_id = "process_raw_data",
            python_callable=turn_dict_raw_df,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_video_id_df = PythonOperator(
            task_id = "process_video_id_df",
            python_callable=turn_dict_dim_video_id,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_channel_title_df = PythonOperator(
            task_id = "process_channel_title_df",
            python_callable=turn_dict_dim_channel_title,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_title_df=PythonOperator(
            task_id="process_dim_title_df",
            python_callable=turn_dict_dim_title,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_timestamp_df = PythonOperator(
            task_id="process_dim_timestamp_df",
            python_callable=turn_dict_timestamp,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_duration_df=PythonOperator(
            task_id="process_dim_duration_df",
            python_callable=turn_dict_duration,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
        process_fact_df = PythonOperator(
            task_id="process_fact_df",
            python_callable=turn_dict_fact,
            op_kwargs={
                "dict":transform_youtube_data.output
            }
        )
    with TaskGroup("write_to_bq") as write_to_bq:

        load_raw_data = PythonOperator(
            task_id = "write_raw_data_bq",
            python_callable=load_raw_df,
            op_kwargs={
                "df":process_raw_data.output,
                "table_id":"youtube-api-388114.youtube_api.raw_data"
                }
            )
        load_dim_video_id_data = PythonOperator(
            task_id="write_video_id_bq",
            python_callable=load_dim_video_id,
            op_kwargs={
                "df":process_video_id_df.output,
                "table_id":"youtube-api-388114.youtube_api.dimension_video_id"
                 }
        )
        load_dim_channel_title_data = PythonOperator(
            task_id = "write_channel_title_bq",
            python_callable=load_dim_channel_title,
            op_kwargs={
                "df":process_channel_title_df.output,
                "table_id":"youtube-api-388114.youtube_api.dimension_channel_title"
            }
        )   

        load_dim_title_data = PythonOperator(
            task_id="write_dim_title_bq",
            python_callable=load_dim_title,
            op_kwargs={
                "df":process_title_df.output,
                "table_id":"youtube-api-388114.youtube_api.dimension_title"
            }
        )

        load_dim_timestamp_data = PythonOperator(
            task_id = "write_dim_timestamp_bq",
            python_callable=load_dim_timestamp,
            op_kwargs={
                "df":process_timestamp_df.output,
                "table_id":"youtube-api-388114.youtube_api.dimension_timestamp"
            }
        )
        load_dim_duration_data = PythonOperator(
            task_id="write_dim_duration_bq",
            python_callable=load_dim_duration,
            op_kwargs={
                "df":process_duration_df.output,
                "table_id":"youtube-api-388114.youtube_api.dimension_duration"
            }
        )

        load_fact_table = PythonOperator(
            task_id = "write_fact_to_bq",
            python_callable=load_fact,
            op_kwargs={
                "df":process_fact_df.output,
                "table_id":"youtube-api-388114.youtube_api.fact_table"
            }
        )

download_youtube_api >> write_csv_to_gcs >> transform_youtube_data
transform_youtube_data >> process_dataframe >> write_to_bq