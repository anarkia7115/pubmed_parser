from unittest import TestCase
import configparser
from stream_reader import obs_reader

config = configparser.ConfigParser()
config.read("config.ini")


class TestObsReader(TestCase):
    def setUp(self) -> None:
        self.obs_reader = obs_reader.ObsReader()

    def test_read_chunk(self):
        one_pubmed_gz_obs = config['PATHS']['one_pubmed_gz_obs_key']
        chunk_size = 10
        print(self.obs_reader.read_chunk(one_pubmed_gz_obs, chunk_size))

        # self.fail()
