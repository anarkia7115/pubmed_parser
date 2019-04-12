import json
from flask import Flask
from flask import request
from stream_parser.pubmed_row_parser import PubmedRowParser
import requests

app = Flask(__name__)


@app.route("/")
def index_page():
    example_str = """
    Example:
    
    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{ "path": "pubmed_baseline/pubmed19n0971.xml.gz", "limit": 10 }' \
      http://localhost:5000/parse_pubmed
    """

    return example_str


@app.route("/parse_pubmed", methods=["POST"])
def parse_pubmed():
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
    pubmed_path = request.get_json()['path']
    ak = request.get_json()['ak']
    sk = request.get_json()['sk']
    callback = request.get_json().get('callback')
    size_limit = request.get_json().get('limit', -1)

    pr_parser = PubmedRowParser()

    pubmed_rows = pr_parser.parse(pubmed_path, ak, sk)
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
