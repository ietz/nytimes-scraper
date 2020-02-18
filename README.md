# nytimes-scraper

[![PyPI](https://img.shields.io/pypi/v/nytimes-scraper)](https://pypi.org/project/nytimes-scraper/)

Scrape article metadata and comments from NYTimes

## Setup
```bash
pip install nytimes-scraper
```

## CLI usage
The scraper will automatically fetch every article and all the user comments published on
[nytimes.com](https://www.nytimes.com/).
Articles are processed month by month, starting with the current month.
For each month, a `{year}-{month}-articles.pickle` and `{year}-{month}-comments.pickle` will be
generated in the current directory.
If the process is restarted, existing outputs will not be overridden and the scraper will continue
at the month where it left off.
To use it, run
```bash
python -m nytimes_scraper <API_KEY>
```

## Programmatic usage
The scraper can also be started programmatically
```python
import datetime as dt
from nytimes_scraper import run_scraper, scrape_month

# scrape february of 2020
article_df, comment_df = scrape_month('<your_api_key>', date=dt.date(2020, 2, 1))

# scrape all articles month by month
run_scraper('<your_api_key>')
```

Alternatively, the `nytimes_scraper.articles` and `nytimes_scraper.comments` modules can be used for more
fine-grained access:
```python
import datetime as dt
from nytimes_scraper.nyt_api import NytApi
from nytimes_scraper.articles import fetch_articles_by_month, articles_to_df
from nytimes_scraper.comments import fetch_comments, fetch_comments_by_article, comments_to_df

api = NytApi('<your_api_key>')

# Fetch articles of a specific month
articles = fetch_articles_by_month(api, dt.date(2020, 2, 1))
article_df = articles_to_df(articles)

# Fetch comments from multiple articles
# a) using the results of a previous article query
article_ids_and_urls = list(article_df['web_url'].iteritems())
comments_a = fetch_comments(api, article_ids_and_urls)
comment_df = comments_to_df(comments_a)

# b) using a custom list of articles
comments_b = fetch_comments(api, article_ids_and_urls=[
    ('nyt://article/316ef65c-7021-5755-885c-a9e1ef2cfdf2', 'https://www.nytimes.com/2020/01/03/world/middleeast/trump-iran-suleimani.html'),
    ('nyt://article/b2d1b802-412e-51f7-8864-efc931e87bb3', 'https://www.nytimes.com/2020/01/04/opinion/impeachment-witnesses.html'),
])

# Fetch comment for one specific article by its URL
comments_c = fetch_comments_by_article(api, 'https://www.nytimes.com/2019/11/30/opinion/sunday/bernie-sanders.html')
```
