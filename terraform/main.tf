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

resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET
    project    = var.project
    location   = var.region
}

locals {
  youtube_data_bucket = "de_youtube_api"
}
