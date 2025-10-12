output "app_service_name" {
  description = "Nome do Service da aplicação"
  value       = kubernetes_service.app_service.metadata[0].name
}

output "mysql_service_name" {
  description = "Nome do Service do MySQL"
  value       = kubernetes_service.mysql.metadata[0].name
}

output "mysql_service_port" {
  description = "Porta do MySQL no cluster"
  value       = kubernetes_service.mysql.spec[0].port[0].port
}

output "app_image_used" {
  description = "Imagem Docker utilizada pela aplicação"
  value       = "tech-challenge-app:latest"
}

output "app_url" {
  description = "URL local para acessar a aplicação"
  value       = "http://localhost:${kubernetes_service.app_service.spec[0].port[0].node_port}"
}
