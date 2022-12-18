from User import User
import time
from kafka import KafkaProducer
from utils import get_kafka_topic, get_bearer_token

if __name__ == '__main__':
    token = get_bearer_token()
    user = User(token)
    if not user.authenticated:
        print('Invalid bearer token')
        exit()
    kafka_topic = get_kafka_topic('raw_tweets_dspp')
    # dspp: Data Stream Processing Project
    port = '9092'
    producer = KafkaProducer(bootstrap_servers=f'localhost:{port}')
    for tweet in user.get_tweets():
        if tweet.lang == 'en':
            print(tweet.text)
            producer.send(kafka_topic, tweet.json().encode('utf-8'))
        time.sleep(1)
