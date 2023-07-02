variable "project" {
    description = "youtube-api-388114"
    type        = string
    default     = "youtube-api-388114"
}

variable "region" {
    description = "Region for GCP resources"
    default     = "europe-west2"
    type        = string
}

variable "storage_class" {
    description = "Storage class type for your bucket"
    default     = "STANDARD"
    type        = string
}

variable "BQ_DATASET" {
    description = "BigQuery Dataset that raw data from GCS will be written"
    type        = string
    default     = "youtube_api"
}

variable "TABLE_NAME_raw" {
    description = "BigQuery Table"
    type        = string
    default     = "raw_data"
}

variable "TABLE_NAME_dim_video_id" {
    description = "BigQuery Table"
    type = string
    default = "dimension_video_id"
  
}

variable "TABLE_NAME_dim_channel_title" {
    description = "BigQuery Table"
    type = string
    default = "dimension_channel_title"
  
}

variable "TABLE_NAME_dim_title" {
    description = "BigQuery Table"
    type = string
    default = "dimension_title"
  
}


variable "TABLE_NAME_dim_timestamp" {
    description = "BigQuery Table"
    type = string
    default = "dimension_timestamp"
  
}

variable "TABLE_NAME_dim_duration" {
    description = "BigQuery Table"
    type = string
    default = "dimension_duration"
  
}

variable "TABLE_NAME_fact" {
    description = "BigQuery Table"
    type = string
    default = "fact_table"
  
}