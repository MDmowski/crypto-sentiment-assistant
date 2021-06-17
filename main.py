import json
import os

from Reddit import Reddit
from StockHistory import StockHistory
from Twitter import Twitter
import pandas as pd

stockHistory = StockHistory()

df = stockHistory.load_data("BTC", 1, "PLN", "365")
print(df)

reddit = Reddit()
reddit_hot = reddit.get_within_timeframe('bitcoin', 'hot', '7d', '1d', 100)
# print(reddit.get_within_timeframe('bitcoin', 'new', '7d', '0d'))
# for post in hot['data']['children']:
#     print(post['data']['selftext'])
with open("reddit_output.jsonl", 'a') as file:
    for record in reddit_hot.json()['data']:
        json.dump(record, file)
        file.write(os.linesep)

twitter = Twitter()
# print(twitter.get_tweets('bitcoin', 'popular', 'en', 50))
