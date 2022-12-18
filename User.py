import tweepy

from utils import get_keywords


class User:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.authenticated = False
        try:
            for _ in self.get_tweets('COVID'):  # Test the token
                break  # If the token is valid, we should enter this loop
        except tweepy.errors.Unauthorized:
            raise Exception('Invalid bearer token')
        self.authenticated = True

    def get_tweets(self, query=None, max_tweets=100, tweet_fields=None):
        if query is None:
            query = get_keywords()
        if isinstance(query, list):
            query = ' OR '.join(query)
        if tweet_fields is None:
            tweet_fields = ['id', 'text', 'author_id', 'created_at', 'lang', 'possibly_sensitive']
        for tweet in tweepy.Paginator(self.client.search_recent_tweets, query=query, max_results=max_tweets,
                                      tweet_fields=tweet_fields).flatten():
            yield tweet
