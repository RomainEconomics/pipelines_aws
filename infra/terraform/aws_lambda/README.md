
## Deploy Lambda function using Terraform

Fetch french twitter trends and store the result in a s3 bucket.

To use it, run :
- terraform init
- terraform plan (it will create the zip file)
- terraform apply


An bearer token (also called access token) is needed to connect to the Twitter API.
urllib3 is used instead of requests to avoid the overhead of installing dependency package.
