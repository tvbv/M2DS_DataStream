import tweepy


def add_keywords(keywords):
    while True:
        keyword = input('Enter a keyword (leave blank to stop): ')
        if keyword == '':
            break
        else:
            keywords.append(keyword)
    return keywords


class User:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.authenticated = False
        try:
            for _ in self.get_tweets('test'):  # Test the token
                break  # If the token is valid, we should enter this loop
        except tweepy.errors.Unauthorized:
            raise Exception('Invalid bearer token')
        self.authenticated = True
        self.default_keywords = ['SNCF', 'retard']

    def get_tweets(self, query=None, max_tweets=100, tweet_fields=None):
        if query is None:
            query = self.ask_keywords()
        if isinstance(query, list):
            query = ' OR '.join(query)
        if tweet_fields is None:
            tweet_fields = ['id', 'text', 'author_id', 'created_at', 'lang', 'possibly_sensitive']
        for tweet in tweepy.Paginator(self.client.search_recent_tweets, query=query, max_results=max_tweets,
                                      tweet_fields=tweet_fields).flatten():
            yield tweet

    def ask_keywords(self):
        while True:
            print(f'Default keywords: {self.default_keywords}')
            print('Select an option:')
            print('1. Add keywords')
            print('2. Create your own list of keywords')
            print('3. Do nothing (use default keywords)')
            option = input('Option: ')
            try:
                option = int(option)
                if option < 1 or option > 3:
                    print('Invalid option. Try again.')
                    continue
                break
            except:
                print('Invalid option. Try again.')
        if option == 1:
            keywords = self.default_keywords
            keywords = add_keywords(keywords)
        if option == 2:
            keywords = []
            while True:
                keywords = add_keywords(keywords)
                if len(keywords) > 0:
                    break
                else:
                    print('You must enter at least one keyword.')
        if option == 3:
            keywords = self.default_keywords
        return keywords
