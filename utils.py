from kafka import KafkaConsumer, KafkaProducer


def get_kafka_topic(default_topic):
    kafka_topic = input(f'Enter the name of the Kafka topic (leave blank to use "{default_topic}"): ')
    if kafka_topic == '':
        kafka_topic = default_topic
    return kafka_topic


def get_kafka_producer(port='9092'):
    return KafkaProducer(bootstrap_servers=f'localhost:{port}', value_serializer=lambda x: x.encode('utf-8'))


def get_kafka_consumer(kafka_topic, port='9092', group_id=None):
    # kafka_topic can be a string or a list of strings
    if group_id is None:
        consumer = KafkaConsumer(bootstrap_servers=f'localhost:{port}', value_deserializer=lambda x: x.decode('utf-8'))
    else:
        consumer = KafkaConsumer(bootstrap_servers=f'localhost:{port}', value_deserializer=lambda x: x.decode('utf-8'),
                                 group_id=group_id)
    consumer.subscribe(kafka_topic)
    return consumer
