from handle_tokens import get_bearer_token
from Client import Client
import time


if __name__ == '__main__':
    token = get_bearer_token()
    client = Client(token)
    for tweet in client.get_tweets():
        print(tweet.text)
        time.sleep(1)
