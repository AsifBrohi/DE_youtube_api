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

![youtube_api_workflow (3) drawio](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/d2ba326e-a0e4-4e00-b8eb-e7d09de2a5fa)


## Airflow DAG

![image](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/3809c7fe-8d60-4a1e-b177-453e93216762)

## Dashboard 

![youtube_dashboard-_2_](https://github.com/AsifBrohi/DE_youtube_api/assets/52333702/40fa06bd-decf-4473-bd77-d45c4e15b4b4)

