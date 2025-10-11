resource "docker_network" "mysql_net" {
  name = "mysql_net"
}

resource "docker_volume" "mysql_data" {
  name = "mysql_data"
}

resource "docker_container" "mysql" {
  name  = "mysql"
  image = "mysql:8.0"

  env = [
    "MYSQL_ROOT_PASSWORD=${var.database_root_password}",
    "MYSQL_DATABASE=${var.database_name}",
    "MYSQL_USER=${var.database_username}",
    "MYSQL_PASSWORD=${var.database_password}"
  ]

  ports {
    internal = 3306
    external = 3306
  }

  volumes {
    container_path = "/var/lib/mysql"
    volume_name    = docker_volume.mysql_data.name
  }

  networks_advanced {
    name = docker_network.mysql_net.name
  }

  restart = "unless-stopped"
}
