provider "google" {
  credentials = file("./mohammed_gkey.json")
  project     = "csci-5409-417319"
  region      = "us-east1"
}

resource "google_container_cluster" "mohammed_cluster" {
  name               = "mohammed-cluster"
  location           = "us-east1"
  initial_node_count = 1

  
  deletion_protection = false

  node_config {
    machine_type        = "e2-micro"
    disk_size_gb        = 10
    disk_type           = "pd-standard"
    image_type          = "COS_CONTAINERD"
    preemptible         = false
    oauth_scopes        = ["https://www.googleapis.com/auth/cloud-platform"]
    metadata            = {
      disable-legacy-endpoints = "true"
    }
  }

  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}
