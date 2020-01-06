import datetime as dt
from pathlib import Path
from typing import Tuple, Callable

import pandas as pd

from nytimes_scraper.articles import fetch_articles_by_month, articles_to_df
from nytimes_scraper.comments import fetch_comments, comments_to_df
from nytimes_scraper.nyt_api import NytApi


out_dir = Path.cwd()


def run_scraper(api_key: str):
    """Scrape articles and comments month by month, starting from the current month"""

    # the year and month to be fetched
    date = dt.datetime.now().date().replace(day=1)
    while True:
        scrape_month(api_key, date)

        # go one month back
        date = (date - dt.timedelta(days=1)).replace(day=1)


def scrape_month(api_key: str, date: dt.date, force_fetch: bool = False, store: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Scrape articles and comments for a given month. The `date.day` is ignored."""

    api = NytApi(api_key)

    article_df = cached(
        fetch=lambda: articles_to_df(fetch_articles_by_month(api, date)),
        file=out_file(date, 'articles'),
        force_fetch=force_fetch,
        store=store,
    )

    article_ids_and_urls = list(article_df['web_url'].iteritems())
    comment_df = cached(
        fetch=lambda: comments_to_df(fetch_comments(api, article_ids_and_urls)),
        file=out_file(date, 'comments'),
        force_fetch=force_fetch,
        store=store,
    )

    return article_df, comment_df


def cached(file: Path, fetch: Callable[[], pd.DataFrame], force_fetch: bool, store: bool) -> pd.DataFrame:
    if not file.exists() or force_fetch:
        df = fetch()

        if store:
            file.parent.mkdir(exist_ok=True)
            df.to_pickle(str(file))

        return df
    else:
        return pd.read_pickle(str(file))


def out_file(date: dt.date, kind: str) -> Path:
    return out_dir / f'{date.year}-{date.month:02d}-{kind}.pickle'

