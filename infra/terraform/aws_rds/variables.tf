
variable "region" {
  default     = "eu-west-3"
  description = "AWS region"
}

variable "db_username" {
  description = "RDS root user name"
  sensitive   = true
}

variable "db_password" {
  description = "RDS root user password"
  sensitive   = true
}
