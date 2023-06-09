# Youtube API

A data pipeline to extract youtube data from using youtube API.

The output is a Google Data Studio report which provides insight into the Channel statistics over period of time.

## Background

Project was based on finding out answers for key questions on a specific YouTube channel 
By leveraging the YouTube API and building a data pipeline, I can automate the process of collecting and analyzing this information, allowing you to gain valuable insights into the performance and audience engagement of the YouTube channel.

## Tools Used 
* **Apache Airflow**
    * I can define your data extraction, transformation, and loading (ETL) processes as workflows using Airflow's Directed Acyclic Graphs (DAGs). Airflow will manage the execution and dependencies of these tasks, ensuring smooth data pipeline operations.
* **Docker**
    * Docker can be used to containerize your data pipeline components. By packaging your application, dependencies, and configurations  into containers, you can ensure consistency and portability across different environments. This allows for easier deployment, scaling, and reproducibility of your data pipeline.
* **Python**
    * Python to interact with the YouTube API, retrieve data, perform data transformations
* **Terraform**
    * Terraform is an infrastructure-as-code tool that allows you to define and manage your infrastructure resources.
      With Terraform, you can define your GCP resources as code using the HashiCorp Configuration Language (HCL). This enables you to version control your infrastructure and easily replicate it across different environments.
      **See Documentation [here](https://github.com/AsifBrohi/DE_youtube_api/blob/main/terraform/README.md)**
* **Google Cloud Storage**
    * Google Cloud Storage (GCS): You can use GCS as a storage solution to store raw data, intermediate outputs, or backup files related to your YouTube channel.
* **Google Bigquery** 
    * BigQuery: BigQuery is a fully managed, serverless data warehouse provided by GCP. It allows you to store and query large amounts of data efficiently. You can use BigQuery to store and analyze the extracted YouTube data, perform complex SQL queries, and generate insights.
* **Google Data Studio**
    * Google Data Studio is a powerful data visualization and reporting tool. It allows you to create interactive and visually appealing dashboards and reports by connecting to various data sources, including BigQuery.

## Database Schema 

After carefully analyzing the raw CSV data from YouTube, a systematic normalization process was performed to transform the data into a highly organized structure following the principles of the 3rd Normal Form. The result of this meticulous effort is a refined schema that optimizes data integrity, reduces redundancy, and improves overall data quality. By normalizing the data, we have achieved a streamlined and efficient representation of the YouTube dataset, enabling more accurate and insightful analysis of key metrics and relationships within the channel's content.

![Model databases - Page 1 (1)](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/208ea18a-5f22-4627-b37a-787c98fc20fd)



## Architecture 

* **Step One**
    * Raw data is extracted using youtube API via python
* **Step Two**
    * Storing raw data as CSV file into GCS bucket 
* **Step Three**
    * Getting the path of CSV file object in GCS bucket and transforming the data , return a dictonary which contains all the dataframes
* **Step Four** 
    * Load data onto bigquery 
* **Step Five**
    * Create a report on Google Data Studio 

![youtube_api_workflow (3) drawio](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/d2ba326e-a0e4-4e00-b8eb-e7d09de2a5fa)


## Airflow DAG

A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.

Shown below is a DAG which contains all the task required for this pipeline and the relationships between each task. 

![image](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/3809c7fe-8d60-4a1e-b177-453e93216762)

### Dag Script
```python
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
```

## BigQuery
Here are some SQL scripts on Bigquery to answer questions about the data
```sql
---- What is the average view count across all videos?
SELECT AVG(viewCount) as avg_viewCount  
FROM `youtube-api-388114.youtube_api.fact_table` f;


---- Which video has the highest view count?
SELECT r.viewCount, r.title
FROM `youtube-api-388114.youtube_api.raw_data` r
WHERE r.viewCount = (SELECT MAX(viewCount) FROM `youtube-api-388114.youtube_api.raw_data`);


---- Calculate the total number of likes for all the videos.
SELECT sum(f.likeCount) as total_likecounts
FROM `youtube-api-388114.youtube_api.fact_table` f
;

---- What is the average duration of the videos?
SELECT avg(t.total_seconds) as avg_total_secs
FROM `youtube-api-388114.youtube_api.dimension_duration` t;

---- Is there a correlation between the duration of a video and its view count?
select d.title,dt.minutes,f.viewCount
FROM `youtube-api-388114.youtube_api.fact_table` f
JOIN `youtube-api-388114.youtube_api.dimension_title`d on f.title_id = d.title_id
JOIN `youtube-api-388114.youtube_api.dimension_duration`dt on f.duration_id = dt.duration_id

ORDER BY viewCount DESC;

---- Calculate the total duration of all the videos combined.
select sum(dt.minutes) as Total_duration_videos
FROM `youtube-api-388114.youtube_api.dimension_duration` dt
;

---- Is there a relationship between the published date of a video and its view count?
SELECT t.date, f.viewCount
FROM `youtube-api-388114.youtube_api.fact_table` f
JOIN `youtube-api-388114.youtube_api.dimension_timestamp` t on f.publishedAt_id = t.publishedAt_id
ORDER BY viewCount DESC
;


---- Compare the view counts and comment counts for each video
SELECT d.title,f.viewCount,f.commentCount
FROM  `youtube-api-388114.youtube_api.fact_table` f
JOIN  `youtube-api-388114.youtube_api.dimension_title` d on f.title_id = d.title_id
;
```

**Created a table using SQL script which will be used for analytics in Google Data Studio**

```sql
CREATE OR REPLACE TABLE `youtube-api-388114.youtube_api.tbl_analytics` as (
SELECT
c.channel_title_id, 
f.video_id_id, 
dt.title,
t.date,
t.time,
d.minutes,
f.likeCount,
f.viewCount,
f.commentCount

from `youtube-api-388114.youtube_api.fact_table` f

JOIN `youtube-api-388114.youtube_api.dimension_channel_title` c on f.channel_title_id=c.channel_title_id
JOIN `youtube-api-388114.youtube_api.dimension_duration` d on f.duration_id=d.duration_id
JOIN `youtube-api-388114.youtube_api.dimension_timestamp` t on f.publishedAt_id=t.publishedAt_id
JOIN `youtube-api-388114.youtube_api.dimension_title` dt on f.title_id=dt.title_id
JOIN `youtube-api-388114.youtube_api.dimension_video_id` v on f.video_id_id=v.video_id_id)
;
```

## Dashboard 

**The Final Output** 

![youtube_dashboard-_2_](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/40fa06bd-decf-4473-bd77-d45c4e15b4b4)

