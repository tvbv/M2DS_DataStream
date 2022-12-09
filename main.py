from handle_tokens import get_bearer_token, remove_token
from Client import Client
import time


if __name__ == '__main__':
    username, token = get_bearer_token()
    try:
        client = Client(token)
        for tweet in client.get_tweets():
            print(tweet.text)
            time.sleep(1)
    except Exception as e:
        print(e)
        remove_token(username)
