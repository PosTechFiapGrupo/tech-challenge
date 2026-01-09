resource "kubernetes_deployment" "app" {
  metadata {
    name = "tech-challenge-app"
    labels = {
      app = "tech-challenge"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "tech-challenge"
      }
    }

    template {
      metadata {
        labels = {
          app = "tech-challenge"
        }
      }

      spec {
        init_container {
          name    = "wait-for-mysql"
          image   = "busybox:latest"
          command = ["sh", "-c", "until nc -z mysql 3306; do echo waiting for mysql; sleep 2; done;"]
        }

        container {
          name              = "tech-challenge"
          image             = "tech-challenge-app:latest"
          image_pull_policy = "Never"

          port {
            container_port = 8000
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 15
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = 8000
            }
            initial_delay_seconds = 10
            period_seconds        = 5
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.app_env.metadata[0].name
            }
          }

          env_from {
            secret_ref {
              name = kubernetes_secret.app_secret.metadata[0].name
            }
          }

          # New Relic Kubernetes metadata
          env {
            name  = "NEW_RELIC_METADATA_KUBERNETES_CLUSTER_NAME"
            value = "tech-challenge-grupo19"
          }

          env {
            name = "NEW_RELIC_METADATA_KUBERNETES_NODE_NAME"
            value_from {
              field_ref {
                field_path = "spec.nodeName"
              }
            }
          }

          env {
            name = "NEW_RELIC_METADATA_KUBERNETES_NAMESPACE_NAME"
            value_from {
              field_ref {
                field_path = "metadata.namespace"
              }
            }
          }

          env {
            name = "NEW_RELIC_METADATA_KUBERNETES_POD_NAME"
            value_from {
              field_ref {
                field_path = "metadata.name"
              }
            }
          }

          env {
            name  = "NEW_RELIC_METADATA_KUBERNETES_CONTAINER_NAME"
            value = "tech-challenge"
          }

          env {
            name  = "NEW_RELIC_METADATA_KUBERNETES_CONTAINER_IMAGE_NAME"
            value = "tech-challenge-app:latest"
          }

          resources {
            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app_service" {
  metadata {
    name = "tech-challenge-svc"
  }

  spec {
    selector = {
      app = "tech-challenge"
    }

    port {
      port        = 8000
      target_port = 8000
      node_port   = 30000
    }

    type = "NodePort"
  }
}
