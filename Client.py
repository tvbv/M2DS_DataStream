import tweepy


def ask_keywords():
    keywords = ''
    while True:
        keywords = input('Enter keywords (separated by a comma) to start querying: ')
        if keywords:
            keywords = keywords.split(',')
            keywords = [keyword.strip() for keyword in keywords]
            keywords = ' OR '.join(keywords)
            return keywords


class Client:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        try:
            for _ in self.get_tweets('test'):  # Test the token
                return  # If the token is valid, we should enter this loop
        except tweepy.errors.Unauthorized:
            raise Exception('Invalid bearer token')

    def get_tweets(self, query=None, max_tweets=100):
        if query is None:
            query = ask_keywords()
        for tweet in tweepy.Paginator(self.client.search_recent_tweets, query=query, max_results=max_tweets).flatten():
            yield tweet
