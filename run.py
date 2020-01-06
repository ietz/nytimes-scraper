import os

from nytimes_scraper import run_scraper

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    api_key = os.environ.get('NYT_API_KEY')
    run_scraper(api_key)
