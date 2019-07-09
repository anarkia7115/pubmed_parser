from kafka import KafkaProducer


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
    except Exception as ex:
        print('Exception in publishing message')
        print("exception: " + str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(2, 2, 0))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


if __name__ == "__main__":
    docs_producer = connect_kafka_producer()
    topic_name = "pubmeds"
    for i in range(1000000, 1000500):
        publish_message(docs_producer, topic_name, str(i), "doc: {}".format(i))
        if i % 100 == 0:
            docs_producer.flush()
            print('100* Message published successfully.')

