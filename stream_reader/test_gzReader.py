from unittest import TestCase
import configparser
from stream_reader import gz_reader

config = configparser.ConfigParser()
config.read("config.ini")


class TestGzReader(TestCase):
    def setUp(self) -> None:
        self.gz_reader = gz_reader.GzReader()

    def test_read(self):
        """
        gunzip takes 1.437s
        this takes only 0.09s

        stream reading the gz

        :return:
        """
        gz_file = config["PATHS"]["one_pubmed_gz"]
        MAX_LINES = 10
        for line_num, content in enumerate(self.gz_reader.read(gz_file), start=1):
            if line_num >= MAX_LINES:
                break
            else:
                print("{}: {}".format(line_num, content))

    def test_read_stream(self):
        some_bytes = b'\x1f\x8b\x08\x08\xd8R\x0f\\\x00\x03'
        print("""
        raw: {}
        decompressed: {}
        """.format(
            some_bytes,
            self.gz_reader.read_stream(some_bytes)
        ))
        # self.fail()

    def test_read_obs_stream(self):
        one_pubmed_gz_obs = config['PATHS']['one_pubmed_gz_obs_key']
        MAX_LINES = 10
        for line_num, content in enumerate(
                self.gz_reader.read_obs_line(one_pubmed_gz_obs), start=1):
            if line_num > MAX_LINES:
                break
            else:
                print("{}: {}".format(line_num, content))

        pubmed_lines = list(self.gz_reader.read_obs_line(one_pubmed_gz_obs))
        print("num of pubmeds: [{}]".format(len(pubmed_lines)))

        # self.fail()
