from time import sleep

import requests

class ArchiveApi:
    def __init__(self, api_key: str, proxies = None):
        self.api_key = api_key
        self.proxies = proxies

    def archive(self, year: int, month: int):
        if self.proxies == None:
            response = requests.get(
                url=f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json',
                params={
                    'api-key': self.api_key,
                },
            )
        else:
            response = requests.get(
                url=f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json',
                proxies = self.proxies,
                verify = False,
                params={
                    'api-key': self.api_key,
                },
            )
        sleep(1)
        return response.json()
