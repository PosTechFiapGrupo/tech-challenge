resource "kubernetes_job" "migrate_db" {
  metadata {
    name = "migrate-db"
  }

  spec {
    template {
      metadata {
        labels = {
          job = "migrate-db"
        }
      }
      spec {
        init_container {
          name    = "wait-for-mysql"
          image   = "busybox:latest"
          command = ["sh", "-c", "until nc -z mysql 3306; do echo waiting for mysql; sleep 2; done;"]
        }

        container {
          name              = "migrate"
          image             = "tech-challenge-app:latest"
          image_pull_policy = "Never"
          command           = ["alembic", "upgrade", "head"]

          env_from {
            config_map_ref {
              name = "app-env"
            }
          }

          env_from {
            secret_ref {
              name = "app-secret"
            }
          }

          volume_mount {
            name       = "env-file"
            mount_path = "/app/.env"
            sub_path   = ".env"
          }
        }

        volume {
          name = "env-file"
          config_map {
            name = "app-env"
          }
        }

        restart_policy = "Never"
      }
    }
  }
}

resource "kubernetes_job" "populate_db" {
  metadata {
    name = "populate-db"
  }

  spec {
    template {
      metadata {
        labels = {
          job = "populate-db"
        }
      }
      spec {
        init_container {
          name    = "wait-for-mysql"
          image   = "busybox:latest"
          command = ["sh", "-c", "until nc -z mysql 3306; do echo waiting for mysql; sleep 2; done;"]
        }

        container {
          name              = "populate"
          image             = "tech-challenge-app:latest"
          image_pull_policy = "Never"
          command           = ["python", "populate_db.py"]

          env_from {
            config_map_ref {
              name = "app-env"
            }
          }

          env_from {
            secret_ref {
              name = "app-secret"
            }
          }

          volume_mount {
            name       = "env-file"
            mount_path = "/app/.env"
            sub_path   = ".env"
          }
        }

        volume {
          name = "env-file"
          config_map {
            name = "app-env"
          }
        }

        restart_policy = "Never"
      }
    }
  }
}
