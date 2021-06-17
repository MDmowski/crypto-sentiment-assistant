import unittest
import datetime as dt
from datetime import datetime

from Reddit import Reddit
from Twitter import Twitter


class TestApiConnections(unittest.TestCase):
    def testRedditAuthentication(self):
        reddit = Reddit()
        response = reddit.authorise()
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['access_token'])

    def testRedditGetHot(self):
        reddit = Reddit()
        response = reddit.get_hot('bitcoin')
        self.assertEqual(200, response.status_code)
        self.assertEqual(50, len(response.json()['data']['children']))

    def testRedditGetHotWithSpecifiedLimit(self):
        reddit = Reddit()
        response = reddit.get_hot('bitcoin', 10)
        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.json()['data']['children']))

    def testRedditGetWithinTimeframe(self):
        reddit = Reddit()
        response = reddit.get_within_timeframe('bitcoin', 'hot', '7d')
        self.assertEqual(200, response.status_code)
        response_data = response.json()['data']
        self.assertEqual(50, len(response_data))
        seq = [row['created_utc'] for row in response_data]
        self.assertTrue(min(seq) >= datetime.timestamp(datetime.now() - dt.timedelta(days=7)))
        self.assertTrue(max(seq) <= datetime.timestamp(datetime.now()))

    def testRedditGetWithinTimeframeWithSpecifiedEnd(self):
        reddit = Reddit()
        response = reddit.get_within_timeframe('bitcoin', 'hot', '7d', '1d')
        self.assertEqual(200, response.status_code)
        response_data = response.json()['data']
        self.assertEqual(50, len(response_data))
        seq = [row['created_utc'] for row in response_data]
        self.assertTrue(min(seq) >= datetime.timestamp(datetime.now() - dt.timedelta(days=7)))
        self.assertTrue(max(seq) <= datetime.timestamp(datetime.now() - dt.timedelta(days=1)))

    def testTwitterAuthorize(self):
        twitter = Twitter()
        twitter.authorise()
        self.assertTrue(twitter.api)

    def testGetTweets(self):
        twitter = Twitter()
        tweets = twitter.get_tweets('bitcoin', 'new', 'en', 100)
        self.assertEqual(100, len(tweets))
