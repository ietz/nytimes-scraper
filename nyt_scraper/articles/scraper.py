import datetime as dt
from typing import List, Dict

from nyt_scraper.nyt_api.api import NytApi


def fetch_articles_by_month(api: NytApi, date: dt.date) -> List[Dict]:
    """Fetch the article metadata for the year-month of `date`"""
    print(f'Fetching articles for {date.year}-{date.month:02d}')
    return api.archive.archive(date.year, date.month)['response']['docs']
