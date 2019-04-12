import configparser
from pubmed_parser import medline_parser
from stream_reader.gz_reader import GzReader

import logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read("config.ini")


class PubmedRowParser(object):

    @staticmethod
    def parse(obs_key, ak, sk):
        gz_reader = GzReader()

        xml_rows = gz_reader.read_obs_line(obs_key, ak, sk)
        xml_string = b"".join(xml_rows)
        logging.info("xml string downloaded")

        logging.info("start to run pubmed parser")
        pubmed_rows = medline_parser.parse_medline_xml(
            xml_string,
            is_string=True
        )
        logging.info("xml string parsed")

        return pubmed_rows
