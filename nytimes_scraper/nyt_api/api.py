from nytimes_scraper.nyt_api.archive import ArchiveApi
from nytimes_scraper.nyt_api.community import CommunityApi


class NytApi:
    def __init__(self, api_key: str, proxies = None):
        self.archive = ArchiveApi(api_key, proxies = proxies)
        self.community = CommunityApi(api_key, proxies = proxies)
