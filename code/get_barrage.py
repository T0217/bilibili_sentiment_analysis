import jieba
import requests
import jieba.analyse
import pandas as pd
import numpy as np
from typing import (
    Dict,
    Tuple,
    List
)
from bs4 import BeautifulSoup
from utils import get_xml_url


def get_barrage(
        url: str,
        headers: Dict[str, str],
        type_: str
) -> pd.DataFrame:

    xml_url = get_xml_url(
        url=url,
        headers=headers
    )
    response = requests.get(
        xml_url,
        headers=headers
    )
    response.encoding = response.apparent_encoding
    xml = response.text

    soup = BeautifulSoup(xml, 'xml')
    content_all = soup.find_all(name='d')

    timeList = []
    contentList = []
    for comment in content_all:
        data = comment.attrs['p']
        if type_ == 'Video':
            time = float(data.split(',')[0])
        elif type_ == 'Real':
            timeStamp = data.split(',')[4]
            time = pd.to_datetime(timeStamp, unit='s')
        else:
            raise TypeError(f'{type_} is not defined.'
                            'Available method are Video, Real.')

        text = comment.text
        timeList.append(time)
        contentList.append(text)

    barrage = pd.DataFrame({'time': timeList,
                            'content': contentList})

    return barrage


def barrage_num(
    barrage_times: pd.Series,
    segment: int
) -> pd.DataFrame:

    num_segment = int(np.ceil(barrage_times.max() / segment))
    segmentDict = {}
    for i in range(num_segment):
        if i == 0:
            start = 0
            end = segment
            segment_range = f'{start}-{end}'
            segmentDict[segment_range] = 0
        else:
            start = segment * i + 1
            end = segment * (i + 1)
            segment_range = f'{start}-{end}'
            segmentDict[segment_range] = 0

    for segment_range in segmentDict.keys():
        start_key = segment_range.split('-')[0]
        end_key = segment_range.split('-')[1]
        for time in barrage_times:
            if int(start_key) <= round(time) <= int(end_key):
                segmentDict[segment_range] = segmentDict[segment_range] + 1

    df_segment = pd.DataFrame(
        data=segmentDict.items(),
        columns=['segment', 'num']
    )

    return df_segment


def top_segment(
        url: str,
        headers: Dict[str, str],
        segment: int
) -> Tuple[pd.DataFrame, List[str]]:

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    df_segment = barrage_num(
        barrage_times=barrage['time'],
        segment=segment
    )
    segment_top_range = df_segment.loc[df_segment['num'].idxmax(), 'segment']

    start = segment_top_range.split('-')[0]
    end = segment_top_range.split('-')[1]
    select_barrage = barrage[(int(start) <= barrage['time']) &
                             (barrage['time'] <= int(end))]

    sentence = '\n'.join(select_barrage['content'])
    allowPOS = ('n', 'nr', 'ns', 'nz', 'v', 'vd', 'vn', 'a', 'q')
    jieba.analyse.set_stop_words('../stopwords.txt')
    keywords = jieba.analyse.textrank(
        sentence,
        topK=10,
        withWeight=False,
        allowPOS=allowPOS
    )

    return select_barrage, keywords


def barrgae_keywords(
        url: str,
        headers: Dict[str, str]
) -> pd.DataFrame:

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    sentence = '\n'.join(barrage['content'])

    allowPOS = ('n', 'nr', 'ns', 'nz', 'v', 'vd', 'vn', 'a', 'q')
    jieba.analyse.set_stop_words('../stopwords.txt')
    keywords = jieba.analyse.textrank(
        sentence,
        topK=10,
        withWeight=True,
        allowPOS=allowPOS
    )
    keywords_df = pd.DataFrame(
        keywords,
        columns=['key', 'value of textrank']
    )

    return keywords_df
