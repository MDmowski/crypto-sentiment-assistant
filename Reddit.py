import json

import requests
from requests.auth import HTTPBasicAuth


class Reddit:
    headers = {'User-Agent': 'BachelorWork/0.0.1'}

    def __init__(self):
        with open("reddit_credentials.json", "r") as file:
            credentials = json.load(file)
        self.CLIENT_ID = credentials['CLIENT_ID']
        self.SECRET_KEY = credentials['SECRET_KEY']
        authentication_response = self.authorise()
        if authentication_response.status_code != 200:
            raise ConnectionError(authentication_response.text)

    def authorise(self):
        with open("reddit_credentials.json", "r") as file:
            credentials = json.load(file)

        auth = HTTPBasicAuth(self.CLIENT_ID, self.SECRET_KEY)

        data = {'grant_type': 'password',
                'username': credentials['username'],
                'password': credentials['password']}

        res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=self.headers)

        self.TOKEN = res.json()['access_token']
        self.headers['Authorization'] = f'bearer {self.TOKEN}'
        return res

    def get_hot(self, subreddit, limit=50):
        url = f'https://oauth.reddit.com/r/{subreddit}/hot'
        return requests.get(url, headers=self.headers, params={'limit': limit-2})

    def get_new(self, subreddit, limit=50):
        url = f'https://oauth.reddit.com/r/{subreddit}/new'
        return requests.get(url, headers=self.headers, params={'limit': limit-2})

    def get_within_timeframe(self, subreddit, sort_by, start, end='0d', limit=50):
        url = f'https://oauth.reddit.com/r/{subreddit}/search?sort={sort_by}'
        return requests.get(f"https://api.pushshift.io/reddit/search/submission/?q={subreddit}&after={start}"
                            f"&before={end}&size={limit}")
