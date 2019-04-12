from unittest import TestCase
import configparser
# from pubmed_parser.pubmed_oa_parser import parse_pubmed_xml
from pubmed_parser.medline_parser import parse_medline_xml


config = configparser.ConfigParser()
config.read("config.ini")


class TestParse_pubmed_xml(TestCase):

    def test_parse_pubmed_xml(self):
        one_pubmed_gz = config["PATHS"]["one_pubmed_gz"]
        output = parse_medline_xml(one_pubmed_gz)
        print(len(output))
        # self.fail()
