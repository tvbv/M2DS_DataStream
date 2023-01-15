import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras import backend as K
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Dense, Activation, Embedding, Dropout, Input, LSTM, Reshape, Lambda, RepeatVector
import tensorflow.keras.layers as layers
tf.random.set_seed(42)
np.random.seed(42)

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
model_rolling = load_model('model_rolling.h5')
topic_data = 'data_stock_raw'

consumer = KafkaConsumer(topic_data, 
                         bootstrap_servers="localhost:9092", 
                         group_id="group-prediction",
                         value_deserializer=json_to_umpy_array)

lenght_min_used_for_prediction = 60
number_point_predicted = 1

plt.ion()


array_stored = []

nombre_prediction = 0
print('ready to predict')
for message in consumer:
    
    model_rolling = load_model('model_rolling.h5')
    if nombre_prediction ==0:
        index_predicted = np.arange(0,len(message.value),1)
    array_received = message.value
    array_stored += array_received.tolist()
    if nombre_prediction >= 1:
        data_close = np.array(array_stored)
        y = []
        x = []
        index = []
        for value_index in range(nombre_prediction*len(array_received),data_close.shape[0]):
            if value_index - int(lenght_min_used_for_prediction/2) < 0:
                pass
            else:
                x.append(data_close[value_index - int(lenght_min_used_for_prediction/2):value_index])
                y.append(data_close[value_index:number_point_predicted+value_index])
                index.append(value_index)


        x = np.array(x)
        x = np.reshape(x, (x.shape[0], x.shape[1],1)).astype('float32')

        y_predicted = model_rolling.predict(x)
        index_predicted = index_predicted + len(array_received) 
        
        plt.plot(index_predicted,y_predicted,color = 'red',label = 'prediction')
        plt.plot(index_predicted,array_received,color = 'blue',label = 'real')
        plt.draw()
        if nombre_prediction==1:
            plt.legend()
            plt.xlabel('n° of sample')
            plt.ylabel('Stock value ($)')
        plt.pause(0.001)
    nombre_prediction+=1

plt.show()

        