import threading, multiprocessing
from kafka import KafkaConsumer, KafkaProducer
from stream_parser.request_processor import Processor

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
        self.request_processor = Processor()
        self.stop_event = multiprocessing.Event()
        self.producer = producer
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_server,
            auto_offset_reset='latest',
            consumer_timeout_ms=60000,  # max 'job run time'/'before next pool' for consumer?
            session_timeout_ms=60001,  # max 'job run time'/'before next pool' for consumer?
            request_timeout_ms=60002,
            # if timeout, reassign to another consumer
            max_poll_records=1,
            group_id=config["KAFKA"]["group_id"])
        self.topic = gz_files_topic

    def stop(self):
        self.consumer.close()

    def start_consuming(self):
        self.consumer.subscribe([self.topic])

        logging.info("consuming: listening to {}".format(self.topic))
        while True:
            for record in self.consumer:
                json_str = record.value.decode('utf-8')
                output_str_gen = self.request_processor.parse_pubmed(json_str)
                #output_str = "processed " + str(record)
                for output_str in output_str_gen:
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

