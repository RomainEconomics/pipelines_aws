import urllib3
import boto3
import json
from datetime import datetime, timezone
import os


def get_twitter_trends():
    """
    Get the 50 top trends for France from Twitter API.
    Returns a list dictionary.
    """    

    def get_request(url, headers, params = {}):
        http = urllib3.PoolManager()
        res = http.request(
            "GET",
            url,
            headers=headers,
            fields=params,
            timeout=5.0,
            retries=urllib3.util.Retry(3)
        )

        res_json = json.loads(res.data.decode("utf8").replace("'", '"'))
        return res_json

    bearer_token = os.getenv('bearer_token')

    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    url = "https://api.twitter.com/1.1/trends/available.json"

    woeids = get_request(url, headers)
    woeid_fr = [ i for i in woeids if i['name'] == 'France' ]
    
    query_params = {"id": woeid_fr[0]["woeid"]}
    url = "https://api.twitter.com/1.1/trends/place.json"
    trends = get_request(url, headers, query_params)
    data = trends[0]['trends'][:50]

    return data


# Store the data in S3
LOCAL_FILE_SYS = "/tmp"

def write_to_local(data, name, loc = LOCAL_FILE_SYS) -> str:
    """
    Write json data to aws lambda local temp file system.
    Send back the file name.
    """
    file_name = loc + "/" + str(name) + ".json"
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

    return file_name


def _get_key() -> str:
    """
    Create date string to update folder name
    """
    dt_now = datetime.now(tz=timezone.utc)
    KEY = (
        dt_now.strftime("%Y-%m-%d")
        + "/"
        + dt_now.strftime("%H")
        + "/"
        + dt_now.strftime("%M")
        + "/"
    )
    return KEY


def write_to_s3(trends_dict, bucket, name = "trends_dict"):
    """
    Takes a list dictionnary, and upload it in a S3 bucket.
    """
    region = os.getenv("region")
    s3 = boto3.client('s3', region_name=region)

    # List buckets
    bucket_response = s3.list_buckets()
    buckets = bucket_response["Buckets"]
    buckets_names = [i['Name'] for i in buckets]

    if bucket in buckets_names:
        print("Bucket exists")
    else:
        print("Bucket does not exist")
        print("Creating bucket")
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)

    key = _get_key()
    file_name = write_to_local(trends_dict, name)
    s3.upload_file(file_name, bucket, key + file_name.split("/")[-1])




