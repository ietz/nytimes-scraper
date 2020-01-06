from typing import List, Dict

import pandas as pd
import pandas.io.json

from nytimes_scraper.comments.util import flatten_replies, remove_reply_references


def comments_to_df(comments: List[Dict]) -> pd.DataFrame:
    all_comments = remove_reply_references(flatten_replies(comments))
    df = pd.io.json.json_normalize(all_comments).set_index('commentID')

    if 'parentID' in df:
        df['parentID'] = df['parentID'].astype(pd.Int64Dtype())

    for col in ['status', 'commentType']:
        if col in df:
            df[col] = df[col].astype(pd.CategoricalDtype())

    for col in ['createDate', 'updateDate', 'approveDate']:
        if col in df:
            df[col] = pd.to_datetime(df[col], unit='s')

    return df
