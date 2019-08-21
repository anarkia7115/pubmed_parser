import json
from stream_parser.pubmed_row_parser import PubmedRowParser

import logging

logging.basicConfig(level=logging.INFO)


class Processor:

    def parse_pubmed(self, json_str):
        """
        curl --header "Content-Type: application/json" \
          --request POST \
          --data '{ "path": "pubmed_baseline/pubmed19n0971.xml.gz", "limit": 10 }' \
          http://localhost:5000/parse_pubmed

        1. read json, get obs path
        2. use read_obs_line to read gz stream
        3. parse stream to pubmed parser

        :return:
        """

        self.pr_parser = PubmedRowParser()

        error_return = ["[ERROR]json decode error"]
        # decode json
        try:
            request = json.loads(json_str)
        except json.decoder.JSONDecodeError as e:
            logging.info("parsing: {}".format(json_str))
            logging.info("ERROR: {}".format(e))
            yield error_return
            return

        # get value from dict by key
        try:
            pubmed_path = request['path']
            # ak = request['ak']
            # sk = request['sk']
        except KeyError as e:
            logging.info("ERROR: key:{} not found".format(e))
            yield error_return
            return

        #callback = request.get_json().get('callback')
        size_limit = request.get('limit', -1)

        try:
            pubmed_rows = self.pr_parser.parse(pubmed_path)
        except Exception as e:
            logging.info("ERROR: \n{}: {}".format(e.__class__, e))
            yield error_return
            return

        if size_limit > 0:
            for pubmed_row in pubmed_rows[:size_limit]:
                pubmed_row["raw_gz"] = pubmed_path
                yield json.dumps(pubmed_row)
        else:
            for pubmed_row in pubmed_rows:
                pubmed_row["raw_gz"] = pubmed_path
                yield json.dumps(pubmed_row)

