import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Dense, Activation, Embedding, Dropout, Input, LSTM, Reshape, Lambda, RepeatVector
import tensorflow.keras.layers as layers

import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import JSONEncoder

tf.random.set_seed(42)
np.random.seed(42)


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
json_to_umpy_array = lambda x: np.array(json.loads(x.decode("utf-8"))['array'])

topic_dataset = 'dataset_to_learn'

# Create the consumer
consumer = KafkaConsumer(topic_dataset,
                         bootstrap_servers="localhost:9092",
                         group_id="group-model-training",
                         value_deserializer=json_to_umpy_array)


def scaler(x, x_ref):
    """
    Scale the data to be between 0 and 1, but has no effect here

    Parameters
    ----------
    x : array
        The data to scale
    x_ref : array
        The reference data to scale

    Returns
    -------
    array
        The scaled data
    """
    return x  # (x-np.mean(x_ref))/np.max(np.abs(x_ref-np.mean(x_ref)))


def unscaler(x, x_ref):
    """
    Unscale the data, but has no effect here

    Parameters
    ----------
    x : array
        The data to unscale
    x_ref : array
        The reference data to unscale

    Returns
    -------
    array
        The unscaled data
    """
    return x  # x*np.max(np.abs(x_ref-np.mean(x_ref)))+np.mean(x_ref)


lenght_min_used_for_prediction = 60
number_point_predicted = 1

# Create the model, with 2 LSTM layers and 2 Dense layers
model_rolling = Sequential([
    LSTM(100, return_sequences=True, input_shape=[int(lenght_min_used_for_prediction / 2), 1]),
    # Dropout(0.3),
    LSTM(100, input_shape=[int(lenght_min_used_for_prediction / 2), 1]),
    Dense(25),  # ,activation='relu'),
    # Dropout(0.3),
    Dense(number_point_predicted)  # ,
    # Activation('sigmoid')
])

model_rolling.build(input_shape=[30, 1])
model_rolling.compile(loss='MSE', optimizer='adam')

model_rolling.save('model_rolling.h5')

# For each message received, train the model
for message in consumer:
    print('data received for training')
    data_close = message.value
    y = []
    x = []
    index = []
    for value_index in range(data_close.shape[0] - number_point_predicted):
        if value_index - int(lenght_min_used_for_prediction / 2) < 0:
            pass
        else:
            x.append(data_close[value_index - int(lenght_min_used_for_prediction / 2):value_index])
            y.append(data_close[value_index:number_point_predicted + value_index])
            index.append(value_index)

    y = np.array(y).astype('float32')

    x = np.array(x)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1)).astype('float32')

    model_rolling.fit(x, y, batch_size=10, epochs=5, verbose=0)
    model_rolling.save('model_rolling.h5')
    print('model trained')
    time.sleep(0.1)
