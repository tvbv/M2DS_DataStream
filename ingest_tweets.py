from handle_tokens import get_bearer_token, add_token
from User import User
import time
from kafka import KafkaProducer
from utils import get_kafka_topic


if __name__ == '__main__':
    username, token, new_user = get_bearer_token()
    user = User(token)
    if not user.authenticated:
        print('Invalid bearer token')
        exit()
    if new_user:
        add_token(username, token)
    kafka_topic = get_kafka_topic('raw_tweets_dspp')
    # dspp: Data Stream Processing Project
    port = '9092'
    producer = KafkaProducer(bootstrap_servers=f'localhost:{port}')
    print(f'Producing tweets to topic {kafka_topic}...')
    all_tweet_fields = ['data', 'id', 'text', 'edit_history_tweet_ids', 'attachments', 'author_id',
                        'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'entities',
                        'geo', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'organic_metrics',
                        'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets',
                        'reply_settings', 'source', 'withheld']
    tweet_fields = ['id', 'text', 'author_id', 'created_at', 'public_metrics', 'lang', 'non_public_metrics',
                    'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics']
    for tweet in user.get_tweets(tweet_fields=tweet_fields):
        producer.send(kafka_topic, tweet.json().encode('utf-8'))
        time.sleep(1)
