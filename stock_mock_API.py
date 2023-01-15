import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from kafka import KafkaProducer
import json
from json import JSONEncoder

# Load the data: stock values of Google from mid-december 2022 to mid-january 2023 (1 minute interval)
GOOG_stock = np.load('data\GOOG_1m_2022-11-17_2023-01-13_array.npy', allow_pickle=True)


class NumpyArrayEncoder(JSONEncoder):
    """
    Special json encoder for numpy arrays
    """

    def default(self, obj):
        """
        Returns the serializable object with the given obj

        Parameters
        ----------
        obj : object
            The object to be serialized

        Returns
        -------
        object
            The serializable object
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


data_to_json_utf8 = lambda x: json.dumps({"array": x}, cls=NumpyArrayEncoder).encode("utf-8")

# Create the producer
producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer=data_to_json_utf8)

topic_name = 'data_stock_raw'


def send_data(data_to_send, producer, topic='data_stock_raw'):
    """
    Send data to kafka topic
    
    Parameters
    ----------
    data_to_send : array
        The data to send
    producer : KafkaProducer
        The producer to send the data
    topic : str
        The topic to send the data
    """
    message = data_to_send
    producer.send(topic, message)


periode_envoi_seconde = 2.5
number_datapoint_sent = 100

index_to_send = 0
print('number of samples to stream : ', len(GOOG_stock))

# Send the data to the topic with a delay of periode_envoi_seconde seconds
while index_to_send <= len(GOOG_stock) - number_datapoint_sent:
    print(index_to_send, ' samples sent')
    send_data(GOOG_stock[index_to_send:index_to_send + number_datapoint_sent], producer, topic_name)
    index_to_send += number_datapoint_sent
    time.sleep(periode_envoi_seconde)
