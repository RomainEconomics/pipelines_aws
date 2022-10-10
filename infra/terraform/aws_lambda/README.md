aws_lambda folder is used to fetch french twitter trends and store the result in a s3 bucket.

Environment variables used :
- S3_BUCKET
- region
- bearer token for the twitter api (in the setup_lambda.sh file)

An bearer token (also called access token) is needed.
We use urllib3 instead of requests to avoid the overhead of installing dependency package.


## Deploy Lambda function using Terraform

Fetch french twitter trends and store the result in a s3 bucket.

To use it, run :
- terraform init
- terraform plan (it will create the zip file)
- terraform apply

Environment variables used :
- S3_BUCKET
- region
- bearer token for the twitter api (in the setup_lambda.sh file)

An bearer token (also called access token) is needed.
urllib3 is used instead of requests to avoid the overhead of installing dependency package.
