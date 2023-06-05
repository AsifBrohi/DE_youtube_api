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
