# New Relic Kubernetes Integration
# Instala o nri-bundle para monitoramento completo do cluster

resource "helm_release" "newrelic" {
  name             = "newrelic-bundle"
  repository       = "https://helm-charts.newrelic.com"
  chart            = "nri-bundle"
  namespace        = "newrelic"
  create_namespace = true

  values = [
    yamlencode({
      global = {
        licenseKey  = lookup(local.env_vars, "NEW_RELIC_LICENSE_KEY", "")
        cluster     = "tech-challenge-grupo19"
        lowDataMode = false
      }
      newrelic-infrastructure = {
        enabled = true
      }
      nri-kube-events = {
        enabled = true
      }
      newrelic-logging = {
        enabled = true
      }
      nri-prometheus = {
        enabled = true
      }
      nri-metadata-injection = {
        enabled = true
      }
      kube-state-metrics = {
        enabled = true
      }
    })
  ]

  # Timeout para instalação do chart
  timeout = 600

  # Aguardar até que todos os recursos estejam prontos
  wait = true

  depends_on = [
    kubernetes_deployment.app
  ]
}
