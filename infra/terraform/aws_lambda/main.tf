terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = "default"
}


resource "aws_iam_role" "lambda_role" {
  name               = "terraform_aws_lambda_role"
  assume_role_policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
    }
  EOF
}

resource "aws_iam_policy" "iam_policy_for_lambda" {
  name        = "aws_iam_policy_for_terraform_aws_lambda"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:CreateLogStream"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets"
      ],
      "Resource": "arn:aws:s3:::*"
    },
        {
      "Action": [
            "s3:GetObject",
            "s3:GetObjectAcl",
            "s3:PutObject"
        ],
      "Effect": "Allow",
      "Resource": [
         "arn:aws:s3:::${var.s3_bucket}",
         "arn:aws:s3:::${var.s3_bucket}/*"
      ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}


data "archive_file" "zip_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/src/" # path.module is the current directory
  output_path = "${path.module}/src/lambda-twitter-trends.zip"
}

resource "aws_lambda_function" "terraform_lambda_function" {
  filename      = "${path.module}/src/lambda-twitter-trends.zip"
  function_name = "terraform-lambda-trends-twitter-fr"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  depends_on = [
    aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role
  ]
  environment {
    variables = {
      region       = var.region
      s3_bucket    = var.s3_bucket
      bearer_token = var.bearer_token
    }
  }
}


resource "aws_cloudwatch_event_rule" "every_four_hours" {
  name                = "every-one-minute"
  description         = "Fires every four hours"
  depends_on = [
    aws_lambda_function.terraform_lambda_function
  ]
  schedule_expression = "rate(4 hours)"
}


resource "aws_cloudwatch_event_target" "check_foo_every_four_hours" {
  rule      = aws_cloudwatch_event_rule.every_four_hours.name
  target_id = "terraform_lambda_function"
  arn       = aws_lambda_function.terraform_lambda_function.arn
}


resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.terraform_lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_four_hours.arn
}

