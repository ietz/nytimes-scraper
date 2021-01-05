from typing import List, Dict

import pandas as pd


def articles_to_df(articles: List[Dict]) -> pd.DataFrame:
    df = pd.json_normalize(articles).set_index('_id')

    if 'pub_date' in df:
        df['pub_date'] = pd.to_datetime(df['pub_date'])

    for col in ['document_type', 'news_desk', 'section_name', 'type_of_material', 'byline.organization', 'subsectoinName']:
        if col in df:
            df[col] = df[col].astype(pd.CategoricalDtype())

    return df[~df.index.duplicated()]
