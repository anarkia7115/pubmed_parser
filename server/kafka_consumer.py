import json
import threading, multiprocessing
from kafka import KafkaConsumer, KafkaProducer

import configparser
import logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read("config.ini")


class Producer:
    def __init__(self, bootstrap_server, pubmeds_topic):
        self.stop_event = threading.Event()
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_server)
        self.topic = pubmeds_topic

    def stop(self):
        self.producer.close()

    def send_result(self, msg):
        self.producer.send(self.topic, msg.encode('utf-8'))


class Consumer:
    def __init__(self, producer: Producer, bootstrap_server, gz_files_topic):
        from stream_parser.pubmed_row_parser import PubmedRowParser
        self.pr_parser = PubmedRowParser()
        self.stop_event = multiprocessing.Event()
        self.producer = producer
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_server,
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000,
            group_id=config["KAFKA"]["group_id"])
        self.topic = gz_files_topic

    def stop(self):
        self.consumer.close()

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

        error_return = ["[ERROR]json decode error"]
        # decode json
        try:
            request = json.loads(json_str)
        except json.decoder.JSONDecodeError as e:
            logging.info("parsing: {}".format(json_str))
            logging.info("ERROR: {}".format(e))
            return error_return

        # get value from dict by key
        try:
            pubmed_path = request['path']
            # ak = request['ak']
            # sk = request['sk']
        except KeyError as e:
            logging.info("ERROR: key:{} not found".format(e))
            return error_return

        #callback = request.get_json().get('callback')
        size_limit = request.get('limit', -1)

        try:
            pubmed_rows = self.pr_parser.parse(pubmed_path)
        except Exception as e:
            logging.info("ERROR: \n{}".format(e))
            return error_return
        if size_limit != -1:
            return [json.dumps(xx) for xx in pubmed_rows[:size_limit]]
        else:
            return [json.dumps(xx) for xx in pubmed_rows]

    def start_consuming(self):
        self.consumer.subscribe([self.topic])

        logging.info("consuming: listening to {}".format(self.topic))
        while True:
            for record in self.consumer:
                json_str = record.value.decode('utf-8')
                output_str_list = self.parse_pubmed(json_str)
                #output_str = "processed " + str(record)
                for output_str in output_str_list:
                    self.producer.send_result(output_str)

                self.consumer.commit()


if __name__ == "__main__":
    import sys
    assert len(sys.argv)> 3
    bootstrap_server = sys.argv[1]
    gz_files_topic = sys.argv[2]
    pubmeds_topic = sys.argv[3]
    p = Producer(bootstrap_server, pubmeds_topic)
    c = Consumer(p, bootstrap_server, gz_files_topic)

    c.start_consuming()

