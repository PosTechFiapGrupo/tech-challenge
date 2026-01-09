locals {
  env_vars = {
    for line in regexall("([^=]+)=(.*)", file("../.env")) :
    trim(line[0], " \n\r\t") => trim(line[1], " \n\r\t")
  }
}


resource "kubernetes_config_map" "app_env" {
  metadata {
    name = "app-env"
  }
  data = local.env_vars
}

resource "kubernetes_secret" "app_secret" {
  metadata {
    name = "app-secret"
  }

  data = {
    MYSQL_ROOT_PASSWORD = base64encode("root_password")
    MYSQL_PASSWORD      = base64encode("tech_password")
    MYSQL_USER          = base64encode("tech_user")
    NEW_RELIC_LICENSE_KEY = base64encode(lookup(local.env_vars, "NEW_RELIC_LICENSE_KEY", ""))
  }

  type = "Opaque"
}
