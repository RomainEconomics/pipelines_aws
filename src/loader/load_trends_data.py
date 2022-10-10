import json 
import boto3
from dataclasses import dataclass
from typing import List
import psycopg2
import os

user=os.getenv("RDS_POSTGRES_USERNAME", "")
password=os.getenv("RDS_POSTGRES_PASSWORD", "")
host=os.getenv("RDS_POSTGRES_HOST", "")
port=int(os.getenv("RDS_POSTGRES_PORT", 5432))

client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "")
)

@dataclass
class Trend:
    date: str
    name: str
    url: str
    promoted_content: str
    query: str
    tweet_volume: int

    def display(self):
        return self.date,self.name,self.url,self.query,self.tweet_volume

def parse_s3_json_obj(obj):
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    return data


def get_trends_from_s3(client, bucket_name):
    response = client.list_objects(Bucket=bucket_name)
    request_files = response["Contents"]
    data = []
    for file in request_files:
        obj = client.get_object(Bucket=bucket_name, Key=file["Key"])
        data_temp = parse_s3_json_obj(obj)
        data_temp = [(Trend(str(file["LastModified"]), **trend).display()) for trend in data_temp]
        data.extend(data_temp)
    return data



connection = psycopg2.connect(user=user,
                              password=password,
                              host=host,
                              port=port)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS twitter_trends")

create_table_query = """CREATE TABLE IF NOT EXISTS twitter_trends (
    date TIMESTAMP, 
    name VARCHAR(255), 
    url VARCHAR(255), 
    query VARCHAR(255), 
    tweet_volume INT
    );
    """
cursor.execute(create_table_query)


postgres_insert_query = """INSERT INTO twitter_trends (date, name, url, query, tweet_volume) VALUES (%s,%s,%s,%s,%s)"""
records_to_insert = get_trends_from_s3(client, "lambda-demo-bucket-twitter")
cursor.executemany(postgres_insert_query, records_to_insert)
connection.commit()


#cursor.execute("""SELECT * FROM twitter_trends""")
#print(cursor.fetchall())
#df = pd.DataFrame(cursor.fetchall(), columns=["date", "name", "url", "query", "tweet_volume"])
#print(df)
cursor.close()
connection.close()