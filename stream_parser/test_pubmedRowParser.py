from unittest import TestCase
from stream_parser.pubmed_row_parser import PubmedRowParser
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class TestPubmedRowParser(TestCase):
    def setUp(self) -> None:
        self.pr_writer = PubmedRowParser()

    def test_parse(self):
        pubmed_path = config["PATHS"]["one_pubmed_gz_obs_key"]
        pr_rows = self.pr_writer.parse(pubmed_path)

        print(len(pr_rows))
        # self.fail()
