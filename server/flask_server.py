import json
from flask import Flask
from flask import request
from stream_parser.pubmed_row_parser import PubmedRowParser
import requests

app = Flask(__name__)


@app.route("/parse_pubmed", methods=["POST"])
def parse_pubmed():
    """
    1. read json, get obs path
    2. use read_obs_line to read gz stream
    3. parse stream to pubmed parser

    :return:
    """
    pubmed_path = request.get_json()['path']
    callback = request.get_json().get('callback')
    size_limit = request.get_json().get('limit', -1)

    pr_writer = PubmedRowParser()

    pubmed_rows = pr_writer.parse(pubmed_path)
    if callback is None:
        if size_limit != -1:
            return json.dumps(pubmed_rows[:size_limit])
        else:
            return json.dumps(pubmed_rows)
    else:
        for row_num, row in enumerate(pubmed_rows, start=1):
            if size_limit != -1 and row_num > size_limit:
                break
            requests.post(callback, data=json.dumps(row))

