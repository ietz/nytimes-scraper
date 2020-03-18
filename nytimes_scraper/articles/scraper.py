import datetime as dt
import re
from typing import List, Dict

import lxml.html
import requests
from tqdm import tqdm

from nytimes_scraper.nyt_api.api import NytApi


def fetch_articles_by_month(api: NytApi, date: dt.date, show_progress: bool = True) -> List[Dict]:
    """Fetch the article metadata for the year-month of `date`"""
    print(f'Fetching articles for {date.year}-{date.month:02d}')

    articles = api.archive.archive(date.year, date.month)['response']['docs']
    for article in tqdm(articles, unit='Article', disable=not show_progress):
        try:
            article['html'] = fetch_article_html(article['web_url'])
            article['text'] = scrape_article_text(article['html'])
        except ValueError:
            pass

    return articles


def fetch_article_html(article_url: str) -> str:
    return requests.get(article_url).text


def scrape_article_text(article_html: str) -> str:
    doc = lxml.html.fromstring(article_html)
    text_nodes = doc.cssselect('section[name="articleBody"] > .StoryBodyCompanionColumn > :first-child > *')
    text_node_contents = [re.sub(r'[\n\s]+', ' ', node.text_content()).strip() for node in text_nodes]
    return '\n'.join(text for text in text_node_contents if text != '')
