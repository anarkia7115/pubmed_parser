import json
from unittest import TestCase
from stream_parser.request_processor import Processor


class TestProcessor(TestCase):
    def test_parse_pubmed(self):
        processor = Processor()
        json_request_str = '{ "path": "pubmed_baseline/pubmed19n0971.xml.gz", "limit": 10 }'
        count = 0

        for pubmed_row in processor.parse_pubmed(json_request_str):
            count += 1
            parsed = json.loads(pubmed_row)
            print(json.dumps(parsed, indent=2, sort_keys=True))

        assert count == 10
