## Pipelines on AWS using Twitter API data

With this project, the idea is to fetch simple data from an API, here using Twitter to get the trending topics,
and used all the different tools and infrastructure available to a data engineer today.

Therefore the focus is on building a robust infrastructure and improve my knowledge using those tools.

### What tools ?

- **Python** as the main programming language
- **AWS** is used as cloud provider
- **Terraform** is used to built the AWS infrastructure (**Lambda** function, **RDS** to build a **Postgres** DB)
- The source of truth will be a **S3** bucket, and the data will be made available from a RDS Postgres DB
- **Docker** to containerize the different applications. Two Python container.
  - one for extracting and loading the data to the RDS database
  - one for a **streamlit** app to display the data available in the RDS database


### Folder organization

- **Containers** : contains the Dockerfile to create the images for the docker container (one to load the data from the S3 bucket, one to display the data available in the RDS database)
- **Infra** : contains the terraform files used to deploy the lambda function and the RDS Postgres database
- **Src** : contains the codes used by the containers
- **Tests** : where all tests for this app will be located
- **Utils** : may be used later to improve the connection to the database

In this folder, the docker-compose file is used to create the containers, from the images generated with the dockerfiles located in the containers folder. Moreover, the Make file is used to speed up the deployment and the connection to the different containers. It will also be useful later, when tests will be implemented.

### What's next ?

- Improve the credentials management
- Improve the management of the DB and the way to connect to it
- Add CI/CD to the Terraform infrastructure and the different apps
- Have a remote storage for the tfstate files
- Add tests (Unit tests and Integration tests)
- Use ECR to host the docker images, and use Fargate or an EC2 instance to deploy the containers
- Add lambda trigger function, to update the RDS DB when S3 bucket is updated
