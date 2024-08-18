import pandas as pd
import numpy as np
from typing import Dict
from snownlp import SnowNLP
from get_barrage import get_barrage


def sentiment_analyse(
        url: str,
        headers: Dict[str, str]
) -> pd.DataFrame:

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    content = list(barrage['content'])

    scoreList = []
    tagList = []
    sentiment_df = pd.DataFrame()

    for comment in content:
        tag = ''
        sentiments_score = SnowNLP(comment).sentiments
        if sentiments_score < 0.5:
            tag = 'negtive'
        elif sentiments_score > 0.5:
            tag = 'positive'
        else:
            tag = 'neutral'
        scoreList.append(round(sentiments_score, 2))
        tagList.append(tag)

    sentiment_df['score'] = scoreList
    sentiment_df['tag'] = tagList

    return sentiment_df


def sentiment_trend(
        url: str,
        headers: Dict[str, str],
        segment: int
) -> pd.DataFrame:

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    sentiment_df = sentiment_analyse(
        url=url,
        headers=headers
    )
    sentiment_df = pd.concat(
        [barrage['time'], sentiment_df],
        axis=1
    )

    times = sentiment_df['time']
    segment = segment
    num_segment = int(np.ceil(times.max() / segment))

    segmentList = []
    for i in range(num_segment):
        if i == 0:
            start = 0
            end = segment
            segment_range = f'{start}-{end}'
            segmentList.append(segment_range)
        else:
            start = segment * i + 1
            end = segment * (i + 1)
            segment_range = f'{start}-{end}'
            segmentList.append(segment_range)

    num_tag = pd.DataFrame(columns=['positive', 'neutral', 'negtive'])
    for segment_range in segmentList:
        start = segment_range.split('-')[0]
        end = segment_range.split('-')[1]
        select_df = sentiment_df[(int(start) <= sentiment_df['time']) &
                                 (sentiment_df['time'] <= int(end))]
        n_tag = pd.DataFrame(select_df['tag'].value_counts()).T
        num_tag = pd.concat([num_tag, n_tag])
    num_tag = num_tag.fillna(0)
    num_tag['segment_range'] = segmentList

    return num_tag
