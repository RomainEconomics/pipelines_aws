from helpers import get_twitter_trends, write_to_s3
import json
import os

def lambda_handler(event, context):
    S3_BUCKET = os.getenv("s3_bucket")

    trends_dict = get_twitter_trends()
    write_to_s3(trends_dict, bucket = S3_BUCKET)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }