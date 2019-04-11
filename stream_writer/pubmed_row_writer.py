import configparser
import boto3

config = configparser.ConfigParser()
config.read("config.ini")


class ObsWriter(object):
    def __init__(self):
        self.s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=config['OBS']['ak'],
            aws_secret_access_key=config['OBS']['sk'],
            endpoint_url=config['OBS']['endpoint'],
        )
        self.bucket = config['OBS']['bucket']

    def write(self, stream_to_write, obs_key):
        raise Exception("Not Implemented Yet!")
