output "database_container_name" {
  value = docker_container.mysql.name
}

output "database_root_password" {
  value     = var.database_password
  sensitive = true
}

output "database_password" {
  value     = var.database_password
  sensitive = true
}

output "database_name" {
  value = var.database_name
}
