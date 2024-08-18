import jieba
import pandas as pd
from typing import Dict
from get_barrage import get_barrage


def count_word_frequency(
        url: str,
        headers: Dict[str, str]
) -> pd.DataFrame:

    barrage = get_barrage(
        url=url,
        headers=headers,
        type_='Video'
    )
    barrage = list(barrage['content'])

    with open('../stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read()

    wordsDict = {}
    for content in barrage:
        temp_text = jieba.cut(content)
        for word in temp_text:
            if (word not in stopwords) and (not word.isdigit()) and\
               (not word.islower()) and (not word.isupper()):
                wordsDict[word] = wordsDict.get(word, 0) + 1
            else:
                pass
    words_frequency = pd.DataFrame(
        wordsDict.items(),
        columns=['word', 'frequency']
    )

    return words_frequency
