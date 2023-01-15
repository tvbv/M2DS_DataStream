import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

data_to_json_utf8 = lambda x : json.dumps({"array": x}, cls=NumpyArrayEncoder).encode("utf-8")
json_to_umpy_array = lambda x : np.array(json.loads(x.decode("utf-8"))['array'])


topic_data = 'data_stock_raw'
topic_dataset = 'dataset_to_learn'

consumer = KafkaConsumer(topic_data, 
                         bootstrap_servers="localhost:9092", 
                         group_id="group-1",
                         value_deserializer=json_to_umpy_array)

producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer = data_to_json_utf8)

def send_data(data_to_send, producer,topic = 'data_set_to_learn'):
    message = data_to_send
    producer.send(topic, message)


array_stored = []
last_batch_sent_index = 0

send_batch_to_learn_every = 480

for message in consumer:
    print('data raw received')
    array_received = message.value
    array_stored += array_received.tolist()
    if len(array_stored)-last_batch_sent_index >= send_batch_to_learn_every:
        print('data for training sent')
        start_index = min(len(array_stored),7*send_batch_to_learn_every)
        dataset_to_send = array_stored[-start_index:]
        send_data(dataset_to_send,producer,topic = topic_dataset) 
        last_batch_sent_index = len(array_stored)
    plt.pause(0.001)

