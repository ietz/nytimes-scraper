import datetime as dt
import re
import time
from typing import List, Dict
import random

import lxml.html
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from tqdm import tqdm

from nytimes_scraper.nyt_api.api import NytApi


def fetch_articles_by_month(api: NytApi, date: dt.date, show_progress: bool = True) -> List[Dict]:
    """Fetch the article metadata for the year-month of `date`"""
    print(f'Fetching articles for {date.year}-{date.month:02d}')

    data = api.archive.archive(date.year, date.month)

    # Check if 'response' key exists in the returned data
    if 'response' not in data:
        raise ValueError(f"Expected 'response' key in the data. Received: {data}")

    articles = data['response']['docs']
    for article in tqdm(articles, unit='Article', disable=not show_progress):
        retries = 3
        for _ in range(retries):
            try:
                article['html'] = fetch_article_html(article['web_url'])
                article['text'] = scrape_article_text(article['html'])
                break  # Exit the loop if successful
            except (ValueError, ConnectionError, Timeout) as e:
                if _ < retries - 1:  # i.e. not the last try
                    wait_time = (2 ** _) + (random.randint(0, 1000) / 1000)  # exponential backoff with jitter
                    print(f"Error fetching article from {article['web_url']}: {e}. Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Failed to fetch article from {article['web_url']} after {retries} attempts. Skipping this article.")
                    continue  # Skip to the next article

    return articles

def fetch_article_html(article_url: str) -> str:
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # Raise an error for bad responses
        if not response.text:
            raise ValueError(f"Empty response received for URL: {article_url}")
        return response.text
    except RequestException as e:
        raise ConnectionError(f"Failed to fetch article HTML due to: {e}")

def scrape_article_text(article_html: str) -> str:
    if not article_html:
        raise ValueError("Received empty HTML content for article.")
    
    doc = lxml.html.fromstring(article_html)
    text_nodes = doc.cssselect('section[name="articleBody"] > .StoryBodyCompanionColumn > :first-child > *')
    text_node_contents = [re.sub(r'[\n\s]+', ' ', node.text_content()).strip() for node in text_nodes]
    return '\n'.join(text for text in text_node_contents if text != '')
