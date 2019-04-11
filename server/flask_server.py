from flask import Flask
from flask import request
from stream_parser.pubmed_row_parser import PubmedRowParser

app = Flask(__name__)


@app.route("/parse_pubmed")
def parse_pubmed():
    """
    1. read json, get obs path
    2. use read_obs_line to read gz stream
    3. parse stream to pubmed parser

    :return:
    """
    pubmed_path = request.get_json()['path']
    pr_writer = PubmedRowParser()

    return pr_writer.parse(pubmed_path)

