# 1er essai avec snsrapper -
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import re
from wordcloud import WordCloud, STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk
import googletrans
from deep_translator import GoogleTranslator

import time

tps1 = time.time()


# nltk.download('vader_lexicon') # required for Sentiment Analysis


# functions
def percentage(part, whole):
    """
    Returns the percentage of a part in a whole

    Parameters
    ----------
    part : int
        The part
    whole : int
        The whole

    Returns
    -------
    float
        The percentage of the part in the whole
    """
    return 100 * float(part) / float(whole)


def remove_emoji(string):
    """
    Remove emojis from a string to help with sentiment analysis

    Parameters
    ----------
    string : str
        The string to remove emojis from

    Returns
    -------
    str
        The string without emojis
    """
    emoji_pattern = re.compile("["
                               u"U0001F600-U0001F64F"  # emoticons
                               u"U0001F300-U0001F5FF"  # symbols & pictographs
                               u"U0001F680-U0001F6FF"  # transport & map symbols
                               u"U0001F1E0-U0001F1FF"  # flags (iOS)
                               u"U00002702-U000027B0"
                               u"U000024C2-U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def clean_tweet(tweet):
    """
    Clean a tweet to help with sentiment analysis

    Parameters
    ----------
    tweet : str
        The tweet to clean

    Returns
    -------
    str
        The cleaned tweet
    """
    tweet = convert_emoticons(tweet)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def nlp_pipeline(text):
    """
    Clean a text to help with sentiment analysis

    Parameters
    ----------
    text : str
        The text to clean

    Returns
    -------
    str
        The cleaned text
    """
    text = remove_emoji(text)
    text = text.lower()
    text = re.sub('https\/\/\S+', '', text)  # Removing hyperlink
    text = re.sub('http\/\/\S+', '', text)  # Removing hyperlink
    text = text.replace('\n', ' ').replace('\r', '')
    text = re.sub('@[A-Za-z0–9]+', 'A ', text)  # Removing @mentions
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)
    return text


def result(positive, neutral, negative, polarity, subjectivity):
    """
    Return the result of the sentiment analysis

    Parameters
    ----------
    positive : float
        The positive score
    neutral : float
        The neutral score
    negative : float
        The negative score
    polarity : float
        The polarity score
    subjectivity : float
        The subjectivity score

    Returns
    -------
    int
        The result of the sentiment analysis
    """
    polarity2 = polarity / 2 + 0.5
    if subjectivity > 0.25:
        if np.abs(positive - polarity) < 0.1:
            return 1  # in that case, textblob and SentimentIntensityAnalyzer are 10% concommittant
        elif np.abs(negative - polarity) < 0.1:
            return -1
        else:
            return 0
    else:
        return 0


keywords = "nyse"
maxTweets = 100
tweets_list = []

# 1/ Using TwitterSearchScraper to scrape data and append tweets to list
# For every tweet, we try to translate it to english and then we clean it
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(keywords).get_items()):
    # for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keywords + ' since:' +  start_time + ' until:' + end_time+ ' -filter:links -filter:replies').get_items()):
    # text = clean_tweet(tweet.rawContent)
    text = nlp_pipeline(tweet.rawContent)

    if i == maxTweets:
        break
    lang = tweet.lang
    try:
        text = GoogleTranslator(source='auto', target='en').translate(text)
    except:
        tweet.lang not in languages and tweet.lang == en

    # print(i, lang, lang == 'en', text)
    tweets_list.append(
        [tweet.date, tweet.id, tweet.rawContent, text, tweet.user.username, tweet.likeCount, tweet.user.displayname,
         tweet.lang])

# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list,
                         columns=['Datetime', 'Tweet Id', 'Text', 'Text_eng', 'Username', 'Like Count', 'Display Name',
                                  'Initial_Language'])

# 2/ Basic sentiment Analysis

# Assigning Initial Values
positive = 0
negative = 0
neutral = 0
# Creating empty lists
tweet_list1 = []
neutral_list = []
negative_list = []
positive_list = []

# Iterating over the tweets in the dataframe to calculate the sentiment
for tweet in tweets_df['Text_eng']:
    tweet_list1.append(tweet)
    analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
    neg = analyzer['neg']
    neu = analyzer['neu']
    pos = analyzer['pos']
    comp = analyzer['compound']

    if neg > pos:
        negative_list.append(tweet)  # appending the tweet that satisfies this condition
        negative += 1  # increasing the count by 1
    elif pos > neg:
        positive_list.append(tweet)  # appending the tweet that satisfies this condition
        positive += 1  # increasing the count by 1
    elif pos == neg:
        neutral_list.append(tweet)  # appending the tweet that satisfies this condition
        neutral += 1  # increasing the count by 1

positive = percentage(positive, len(tweets_df))  # percentage is the function defined above
negative = percentage(negative, len(tweets_df))
neutral = percentage(neutral, len(tweets_df))
maxi = np.max([positive, neutral, negative])
if positive == maxi:
    print(1)
elif negative == maxi:
    print(-1)
else:
    print(0)

tps2 = time.time()
print("temps d'execution: ", tps2 - tps1)
# 3_higher level of sentiment analysis : getting the polarity and the subjectivity

# UNDER PROGRESS


# printing the results
# Converting lists to pandas dataframe
# tweet_list1 = pd.DataFrame(tweet_list1)
# neutral_list = pd.DataFrame(neutral_list)
# negative_list = pd.DataFrame(negative_list)
# positive_list = pd.DataFrame(positive_list)
# using len(length) function for counting
# print("Since " + start_time + " days, there have been", len(tweet_list1) ,  "tweets on " + keywords, end='\n*')
# print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
# print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
# print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')

# 2nd essai avec tweepy
'''
import tweepy
import datetime as dt
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAO1WkAEAAAAAcI5932C0xKirVcP5hKs56BW59ME%3DpyK1fCqZjqaVFCJKjiLYf6i2sLtJmQRnmWToXwi056OAdoYa7R')



query = 'NYSE -is:retweet'

# Replace the limit=100 with the maximum number of Tweets you want
for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
    tweet_fields=[ 'created_at', 'lang'], max_results=100).flatten(limit=100):
    print(tweet, tweet['lang'])
    print('\n')

    
start_time = dt.datetime.now() - dt.timedelta( seconds = 10)
espace= dt.timedelta(hours = 1) #we add 10s as the basic access to twitter is only possible with a 10s-delay
end_time = start_time - espace
start_time = start_time.strftime('%H:%M:%S')
end_time = end_time.strftime('%H:%M:%S')
print('intervalle de temps considéré : ',start_time, "jusqu'à", end_time)   



#start_time = '2019-01-01T00:00:00Z'
#end_time = '2020-08-01T00:00:00Z'
start_time = dt.datetime.now() - dt.timedelta( minutes = 1)
end_time = dt.datetime.now() - dt.timedelta(hours = 1)
start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
print('intervalle de temps considéré : ',start_time, "jusqu'à", end_time) 

for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, start_time=start_time,end_time=end_time, max_results=100).flatten(limit=1000):
    final=traductor.translate(tweet.full_text)
    textosinp= final.replace("´","").replace(".","").replace("\n", "")
    assembled="".join(textosinp)
    final2= assembled.rstrip()
    print (final2 )
    archivo.write(final2 +"\n")
'''

# 3e essai mais droits d'accès à la V1 non ouverts!
'''
import requests
import requests_oauthlib
import json

CONSUMER_KEY = 'ssI5qjaAlAzRmNWWwOPzwFL0w'
CONSUMER_SECRET = '7lbWD9U13EClI9picVUVmEp771r2qcEpTRlwH6MfiIwViEd8xU'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAO1WkAEAAAAAcI5932C0xKirVcP5hKs56BW59ME%3DpyK1fCqZjqaVFCJKjiLYf6i2sLtJmQRnmWToXwi056OAdoYa7R'
ACCESS_TOKEN = '1593994709600460801-1mLo9cPHUmQF9qdJFdzkk7vlyqLGd8'
ACCESS_SECRET = '5ipE42U6HwB9L8snasnsr3ZUE0q6yTq6UfxGgxhGF3NFh'

my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def get_tweets():
    #url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    now = dt.datetime.now() - dt.timedelta( seconds = 10)
    espace= dt.timedelta(hours = 1) #we add 10s as the basic access to twitter is only possible with a 10s-delay
    date = now - espace
    now = now.strftime('%H:%M:%S')
    date = date.strftime('%H:%M:%S')
    print('intervalle de temps considéré : ',date, "jusqu'à", now)
    query_data = [('language', 'en', 'fr'), ('locations', '-160,-70,160,80'), ('track','NYSE')]
    #query_data = [('language', 'en', 'fr'), ('locations', '-160,-70,160,80'), ('time', 'date', 'espace'),('track','NYSE', 'nyse')]

    
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response

response = get_tweets()
for line in response.iter_lines():
    full_tweet = json.loads(line)
    print(full_tweet)
    #tweet_text = str(full_tweet['text'])+ "\n"
    #print("Tweet Text: " + tweet_text)
    print ("------------------------------------------")
'''
