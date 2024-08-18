import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import set_path
from PIL import Image
from wordcloud import WordCloud


def visualize_barrage_num(
        data: pd.DataFrame,
        segment: int,
        save: bool,
        savepath: str = None
) -> None:

    num_segment = data.shape[0]
    plt.figure(figsize=(15, 8))
    plt.plot(
        data['segment'], data['num'], marker='o'
    )

    plt.xticks(np.arange(num_segment), np.arange(1, num_segment + 1))
    plt.xlabel(
        f'Segments (The length of one segment is {segment})',
        labelpad=10, size=15
    )
    plt.ylabel('Number', labelpad=10, size=15)
    plt.title('Number of each segment', pad=13, size=18)

    num_top_two = data['num'].nlargest(2)
    for i, value in zip(num_top_two.index, num_top_two):
        plt.text(
            i, value + 3,
            value,
            ha='center', va='bottom',
            fontdict={'size': 13}
        )
    if save:
        savepath = set_path(savepath)
        plt.savefig(savepath, dpi=1000)
    else:
        plt.show()


def visualize_sentiment_trend(
        data: pd.DataFrame,
        segment: int,
        save: bool,
        savepath: str = None
) -> None:

    plt.figure(figsize=(15, 8))
    plt.plot(
        data['segment_range'].astype('str'),
        data['positive'],
        label='positive'
    )
    plt.plot(
        data['segment_range'].astype('str'),
        data['neutral'],
        label='neutral'
    )
    plt.plot(
        data['segment_range'].astype('str'),
        data['negtive'],
        label='negtive'
    )

    plt.xticks(np.arange(data.shape[0]), np.arange(1, data.shape[0] + 1))
    plt.xlabel(
        f'Segments (The length of one segment is {segment})',
        labelpad=10, size=15
    )
    plt.ylabel('Number', labelpad=10, size=15)
    plt.title('Sentiment Trend Chart', pad=13, size=18)
    plt.legend()

    if save:
        savepath = set_path(savepath)
        plt.savefig(savepath, dpi=1000)
    else:
        plt.show()


def generate_word_cloud(
        data: pd.DataFrame,
        mask: bool,
        maskpath: str,
        save: bool,
        savepath: str
) -> None:

    if mask and maskpath:
        maskpath = maskpath
        bgPicture = np.array(Image.open(maskpath))
    else:
        bgPicture = None

    with open('../stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read()

    fontpath = '../fonts/微软雅黑.ttf'

    wc = WordCloud(background_color='white',
                   max_words=2000,
                   mask=bgPicture,
                   stopwords=stopwords,
                   font_path=fontpath,
                   width=1000,
                   height=600)
    wfDict = data.set_index(['word'])['frequency'].to_dict()
    wc.generate_from_frequencies(wfDict)

    if save:
        savepath = set_path(savepath)
        wc.to_file(savepath)
    else:
        plt.figure(figsize=(15, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.show()
