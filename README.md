<h1 align="center">Bilibili Sentiment Analysis</h1>
<p align="center"><strong>基于B站弹幕评论的舆情分析，B站的弹幕的获取，情感分析和词云图</strong></p>

## 一、代码示例

```python
from main import main

# Set parameters
url = 'https://www.bilibili.com/video/BV1wq4y1s7S5/?spm_id_from=333.337.search-card.all.click&vd_source=1d24f52164a3ed510e0b7386c010cc2e'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple\
           WebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
resultpath = './result'

# Run the main function
main(
    url=url,
    headers=headers,
    segment=15,
    save_fig=True,
    resultpath=resultpath
)
```

>   [!IMPORTANT]
>
>   ***如果遇到有关代码的问题或是其他需求，请提 `Issues` 或 `PR` ，我会尽快解决！***

>   [!WARNING]
>
>   ***本项目仅用于学习使用！！！***
>
>   ***本项目仅用于学习使用！！！***
>
>   ***本项目仅用于学习使用！！！***


## 二、思路

### （一）数据获取

-   使用`API接口`获取弹幕数据。

-   获取数据格式为`XML`格式。

### （二）数据分析

#### 1. 视频播放中弹幕发出时间和数量

1.   提取获得的`XML`文件中的节点，得到评论发出时的**视频播放时长**。
2.   分箱，获得某一时段内的弹幕的数量。
3.   可视化。
4.   对弹幕数量最多的部分进行进一步分析。
     -   视频中的内容的分析
         -   文字解释
     -   该段时间的弹幕内容的分析
         -   关键词提取 `(TextRank)`

#### 2. 弹幕实际发出的时间

1.   提取获得的`XML`文件中的节点，得到评论发出时的**实际时间**。**（`XML`格式提取的格式为时间戳）**

2.   根据不同时间节点的弹幕的数量和内容，可结合该时点的新闻或发布的政策等进行分析。

#### 3. 弹幕内容

1.   情感分析
     -   所有弹幕的情感倾向
     -   情感趋势图
2.   关键词提取
3.   词云图

#### 4. 挖掘潜在信息

1.   弹幕与视频内容之间的关联性。
2.   用户在特定事件（如视频中的某个情节）发生时的弹幕行为。
3.   用户之间的互动行为，如回复、@等。

