import time
from kafka import KafkaConsumer


def connect_kafka_consumer(topic_name):
    _consumer = KafkaConsumer(
        topic_name,
        auto_offset_reset='earliest',
        bootstrap_servers=['localhost:9092'], api_version=(2, 2, 0), consumer_timeout_ms=1000)

    return _consumer


def consume_and_print(consumer):
    count = 0
    for msg in consumer:
        count+=1
        #print("msg in consumer: {}".format(msg))
        if count % 100 == 0:
            print("{} messages consumed".format(count))

    print("{} messages consumed".format(count))


if __name__ == "__main__":
    topic_name = "pubmeds"
    docs_consumer = connect_kafka_consumer(topic_name)
    consume_and_print(docs_consumer)
    docs_consumer.close()

