from time import sleep

import requests


class CommunityApi:
    def __init__(self, api_key: str, proxies = None):
        self.api_key = api_key
        self.proxies = proxies

    def get_comments(self, article_url: str, limit: int = 100, offset: int = 0, sort: str = 'oldest'):
        if self.proxies == None:
            response = requests.get(
                url='https://www.nytimes.com/svc/community/V3/requestHandler',
                params={
                    'cmd': 'GetCommentsAll',
                    'url': article_url,
                    'sort': sort,
                    'limit': limit,
                    'offset': offset,
                },
            )
        else:
            response = requests.get(
                url='https://www.nytimes.com/svc/community/V3/requestHandler',
                proxies = self.proxies,
                verify = False,
                params={
                    'cmd': 'GetCommentsAll',
                    'url': article_url,
                    'sort': sort,
                    'limit': limit,
                    'offset': offset,
                },
            )
        sleep(1)
        return response.json()

    def get_replies(self, article_url: str, comment_sequence: int, limit: int = 100, offset: int = 0):
        if self.proxies == None:
            response = requests.get(
                url='https://www.nytimes.com/svc/community/V3/requestHandler',
                params={
                    'cmd': 'GetRepliesBySequence',
                    'url': article_url,
                    'commentSequence': comment_sequence,
                    'limit': limit,
                    'offset': offset,
                },
            )
        else:
            response = requests.get(
                url='https://www.nytimes.com/svc/community/V3/requestHandler',
                proxies = self.proxies,
                verify = False,
                params={
                    'cmd': 'GetRepliesBySequence',
                    'url': article_url,
                    'commentSequence': comment_sequence,
                    'limit': limit,
                    'offset': offset,
                },
            )
        sleep(1)
        return response.json()
