from typing import List, Dict, Optional, Tuple

from tqdm import tqdm

from nytimes_scraper.comments.util import flatten_replies
from nytimes_scraper.nyt_api.api import NytApi


def fetch_comments(api: NytApi, article_ids_and_urls: List[Tuple[str, str]], show_progess: bool = True, pagination_size: int = 100) -> List[Dict]:
    """Fetch all comments from multiple articles, given a list of article IDs and URLs
    `[(id_1, url_1), (id_2, url_2), …]`

    The IDs are not used for processing but are added to the comment objects as an attribute for
    later reference."""

    comments = []
    for article_id, article_url in tqdm(article_ids_and_urls, unit='Article', disable=not show_progess):
        comments.extend(fetch_comments_by_article(api, article_url, article_id=article_id, pagination_size=pagination_size))

    return comments


def fetch_comments_by_article(api: NytApi, article_url: str, article_id: Optional[str] = None, pagination_size: int = 100) -> List[Dict]:
    """Fetch all comments from one specific article"""

    comments = fetch_top_level_comments(api, article_url, pagination_size=pagination_size)
    fetch_replies(api, article_url, comments, pagination_size=pagination_size)

    if article_id is not None:
        for comment in flatten_replies(comments):
            comment['articleID'] = article_id

    return comments


def fetch_top_level_comments(api: NytApi, article_url: str, pagination_size: int) -> List[Dict]:
    """Fetch all top level comments by paginating through the comment list.
    Might also include some replies."""

    comments = []
    while True:
        response = api.community.get_comments(article_url, offset=len(comments), limit=pagination_size)
        if response['status'] != 'OK':
            # some multimedia articles dont allow comments and instead throw an error here
            return []

        results = response['results']
        new_comments = results['comments']
        comments.extend(new_comments)

        if len(new_comments) < pagination_size or len(comments) >= results['totalParentCommentsFound']:
            return comments


def fetch_replies(api: NytApi, article_url: str, comments: List[Dict], pagination_size: int):
    """Fetch all replies for every comment.
    Modifies the comment objects by extending the reply lists."""

    comment_reply_queue = flatten_replies(comments)
    while len(comment_reply_queue) > 0:
        comment = comment_reply_queue.pop()

        while len(comment['replies']) < comment['replyCount']:
            response = api.community.get_replies(
                article_url=article_url,
                comment_sequence=comment['commentSequence'],
                offset=len(comment['replies']),
            )
            results = response['results']

            replies = results['comments'][0]['replies']
            comment['replies'].extend(replies)

            comment_reply_queue.extend(flatten_replies(replies))

            if len(replies) < pagination_size:
                break
