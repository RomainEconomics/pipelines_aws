variable "region" {
  description = "The AWS region to use"
  default = "eu-west-3"
}

variable "s3_bucket" {
  description = "Value of the s3 bucket"
  sensitive   = true
}

variable "bearer_token" {
  description = "Bearer token for Twitter API. Used to fetch the trends"
  sensitive   = true
}