import re
import time
import warnings
import os
from os.path import join, exists
import pandas as pd
from typing import Dict
from utils import (
    set_path,
    get_xml_url
)
from get_barrage import (
    get_barrage,
    barrage_num,
    top_segment,
    barrgae_keywords
)
from sentiment_analyse import (
    sentiment_analyse,
    sentiment_trend
)
from visualize import (
    visualize_barrage_num,
    visualize_sentiment_trend,
    generate_word_cloud
)
from word_frequency import count_word_frequency

# Ignore warnings
warnings.filterwarnings('ignore')


def main(
        url: str,
        headers: Dict[str, str],
        save_fig: bool,
        segment: int = 15,
        maskpath: str = None,
        mask: bool = False,
        resultpath: str = None
) -> None:

    start_time = time.time()

    xml_url = get_xml_url(
        url=url,
        headers=headers
    )
    cid = re.findall(r'com/(.*).xml', xml_url)[0]
    resultpath = set_path(resultpath)
    resultpath = join(resultpath, cid)
    if not exists(resultpath):
        os.makedirs(resultpath)

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    df_segment = barrage_num(
        barrage_times=barrage['time'],
        segment=segment
    )
    visualize_barrage_num(
        data=df_segment,
        segment=segment,
        save=save_fig,
        savepath=join(resultpath, 'barrage_num.png')
    )

    # Get the content of the part with the largest number of barrage
    # And the top ten keywords with the highest weight
    top_segment_text, top_segment_keywords = top_segment(
        url=url,
        headers=headers,
        segment=segment
    )

    top_segment_text.to_csv(
        join(resultpath, 'top_segment_barrage.csv'),
        index=False
    )

    with open(join(resultpath, 'top_segment_keywords.txt'), 'w') as f:
        for keyword in top_segment_keywords:
            f.write(f'{keyword}\n')

    # Get the actual time of the barrage and the content of it
    real_time_barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Real'
    )

    real_time_barrage.to_csv(
        join(resultpath, 'real_time_barrage.csv'),
        index=False
    )

    # sentiment analyse
    sentiment_df = sentiment_analyse(
        url=url,
        headers=headers
    )
    sentiment_df = pd.concat([barrage['content'], sentiment_df], axis=1)
    sentiment_df.to_csv(
        join(resultpath, 'sentiment_trend.csv'),
        index=False
    )

    # sentiment trend
    num_tag = sentiment_trend(
        url=url,
        headers=headers,
        segment=segment
    )
    visualize_sentiment_trend(
        data=num_tag,
        segment=segment,
        save=save_fig,
        savepath=join(resultpath, 'sentiment_trend.png')
    )

    # Keyword extraction for full text
    keywords_df = barrgae_keywords(
        url=url,
        headers=headers
    )
    keywords_df.to_csv(
        join(resultpath, 'barrage_keywords.csv'),
        index=False)

    # Word cloud
    words_frequency = count_word_frequency(
        url=url,
        headers=headers
    )
    generate_word_cloud(
        data=words_frequency,
        mask=mask,
        maskpath=maskpath,
        save=save_fig,
        savepath=join(resultpath, 'word_cloud.png')
    )

    end_time = time.time()

    print('-' * 30 + 'Finished' + '-' * 30)
    print('Total time used: %.2f seconds.' % (end_time - start_time))
