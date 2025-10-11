variable "database_root_password" {
  type        = string
  description = "Senha do usuário root do MySQL"
  default     = "root_password"
}

variable "database_password" {
  type        = string
  description = "Senha do usuário padrão do banco"
  default     = "tech_password"
}

variable "database_username" {
  type        = string
  description = "Nome do banco padrão"
  default     = "tech_user"
}

variable "database_name" {
    type        = string
    description = "Nome do banco padrão"
    default     = "tech_challenge"
}
