terraform {
  required_version = ">=1.0"
  backend "local" {}
  required_providers {
    google = {
        source = "hashicorp/google"
    }
  }
}

provider "google" {
    project = var.project
    region = var.region
}

resource "google_storage_bucket" "youtube_data_bucket" {
    name                        = "${local.youtube_data_bucket}"
    location                    = var.region
    storage_class               = var.storage_class
    uniform_bucket_level_access = true
    
    versioning {
      enabled = true
    }

    lifecycle_rule {
      action {
        type = "Delete"
      }
      condition {
        age = 30
      }
    }

    force_destroy = true
}
resource "google_storage_bucket_iam_member" "youtube_data_bucket" {
  bucket = google_storage_bucket.youtube_data_bucket.name
  role = "roles/storage.objectViewer"
  member = "allUsers"
  
}

resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET
    project    = var.project
    location   = var.region
   
}


resource "google_bigquery_table" "raw_table" {
  table_id = var.TABLE_NAME_raw
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    {
      "name":"video_id",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The video ids of the youtube channel"
    },

    {
      "name":"channelTitle",
      "type":"STRING",
      "mode": "REQUIRED",
      "description":"The channel name"
    },

    {
      "name":"title",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The title of the videos"

    },
    
    {
      "name":"publishedAt",
      "type":"DATETIME",
      "mode":"REQUIRED",
      "description":"When the video was published"
    },
    
    {
      "name":"viewCount",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"Amount of views on a video"

    },

    {
      "name":"likeCount",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"Amount of likes on a video"
    },

    {
      "name":"commentCount",
      "type":"BIGNUMERIC",
      "mode":"NULLABLE",
      "description":"Amount of comments on a video"
    },

    {
      "name":"duartion",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The duration of the video but has not been sorted into mins and seconds"

    },

    {
      "name":"definition",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The quality of the video"
    },

    {
      "name":"caption",
      "type":"STRING",
      "mode":"REQUIRED",
      "descriprion":"Caption is true"
    }

  ]
EOF  

}
resource "google_bigquery_table" "dimension_video_id" {
  table_id = var.TABLE_NAME_dim_video_id
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    { 
      "name":"video_id_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"Video_ids"
    },

    {
      "name":"video_id",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"Video_ids"
    }
  ]
EOF  
}

resource "google_bigquery_table" "dim_channel_title" {
  table_id = var.TABLE_NAME_dim_channel_title
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    {
      "name":"channel_title_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"The channel title id"
      
    },
    {
      "name":"channel_title",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The channel title"
    }

  ]
EOF 
}
resource "google_bigquery_table" "dimension_title" {
  table_id = var.TABLE_NAME_dim_title
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    {
      "name":"title_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"The title id"
      
    },
    {
      "name":"title",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"The title"
    }

  ]
EOF 
  
}

resource "google_bigquery_table" "dimension_timestamp" {
  table_id = var.TABLE_NAME_dim_timestamp
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    {
      "name":"publishedAt_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"ID of video being publishedAt"

    },
    {
      "name":"publishedAt",
      "type":"TIMESTAMP",
      "mode":"REQUIRED",
      "description":"Time&day in which video was published"
    },
    {
      "name":"dates",
      "type":"DATE",
      "mode":"REQUIRED",
      "description":"date video was published"
    },

    {
      "name":"time",
      "type":"TIME",
      "mode":"REQUIRED",
      "description":"Time in which video was published"
    }
  ]
EOF  
}

resource "google_bigquery_table" "dimension_duration" {
  table_id = var.TABLE_NAME_dim_duration
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    {
      "name":"duration_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED",
      "description":"The ID of durations"

    },
    {
      "name":"duration",
      "type":"STRING",
      "mode":"REQUIRED",
      "description":"Duration code"
    },
    {
      "name":"minutes",
      "type":"NUMERIC",
      "mode":"NULLABLE",
      "description":"Number of mins on a video"
    },
    {
      "name":"seconds",
      "type":"NUMERIC",
      "mode":"NULLABLE",
      "description":"Number of secs on a video"
    },
    {
      "name":"total_seconds",
      "type":"BIGNUMERIC",
      "mode":"NULLABLE",
      "description":"Total number of secs on a video"
    }
  ]
EOF  
}

resource "google_bigquery_table" "fact_table" {
  table_id = var.TABLE_NAME_fact
  dataset_id = var.BQ_DATASET
  schema = <<EOF
  [
    { 
      "name":"video_id_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"
    },
    {
      "name":"channel_title_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"
    },
      {

      "name":"title_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"
      },
    {
      "name":"duration_id",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"

    },
    {
      "name":"viewCount",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"

    },
    {
      "name":"likeCount",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"

    },
    {
      "name":"commentCount",
      "type":"BIGNUMERIC",
      "mode":"REQUIRED"

    }
  ]
EOF  
}

locals {
  youtube_data_bucket = "de_youtube_api"
}
