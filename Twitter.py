import tweepy
import json


class Twitter:
    api = None

    def __init__(self):
        self.api = None
        self.authorise()

    def authorise(self):
        with open("twitter_credentials.json", "r") as file:
            credentials = json.load(file)

        auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
        auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

        self.api = tweepy.API(auth)

    def get_tweets(self, query, result_type, language='en', number_of_items=100):
        cursor = tweepy.Cursor(self.api.search, q=query, result_type=result_type, lang=language).items(number_of_items)
        tweets = []
        for tweet in cursor:
            tweets.append(tweet)

        return tweets
