from time import sleep

import requests


class ArchiveApi:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def archive(self, year: int, month: int):
        response = requests.get(
            url=f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json',
            params={
                'api-key': self.api_key,
            },
        )

        sleep(1)
        return response.json()
