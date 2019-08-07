import os
import configparser
import boto3

config = configparser.ConfigParser()
config.read("config.ini")


class ObsReader(object):
    def __init__(self):

        self.s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=os.getenv("AK"),
            aws_secret_access_key=os.getenv("SK"),
            endpoint_url=config['OBS']['endpoint'],
        )
        self.bucket = config['OBS']['bucket']

    def read_chunk(self, obs_key, chunk_size):
        obj = self.s3_client.get_object(
            Bucket=self.bucket,
            Key=obs_key)
        return obj.get("Body").read(chunk_size)

    def read_obj(self, obs_key):
        obj = self.s3_client.get_object(
            Bucket=self.bucket,
            Key=obs_key)
        return obj.get("Body")

