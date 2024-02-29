# bilibili Sentiment Analysis

**基于B站弹幕评论的舆情分析，B站的弹幕的获取，情感分析和词云图**

## 一、代码解释

代码中所参考的代码和文章：*[引用](##三、参考)*

[示例代码](code/demo.py)

[主函数代码](code/main.py)

[自定义函数代码](code/function.py)

[reruirements](requirements.txt)

## 二、思路

### （一）数据获取

-   使用`API接口`获取弹幕数据。

-   获取数据格式为`XML`格式。

### （二）数据分析

#### 1.视频播放中弹幕发出时间和数量

1.   提取获得的`XML`文件中的节点，得到评论发出时的视频播放时长。

2.   分箱，获得某一时段内的弹幕的数量。

3.   可视化。

4.   对弹幕数量最多的部分进行进一步分析。
     -   视频中的内容的分析
         -   文字解释
     -   该段时间的弹幕内容的分析
         -   关键词提取`（Top 10)`

#### 2.弹幕实际发出的时间

1.   提取获得的`XML`文件中的节点，得到评论发出时的实际时间。**（`XML`格式提取的格式为时间戳）**

2.   根据不同时间节点的弹幕的数量和内容，可结合该时点的新闻或发布的政策等进行分析。

#### 3.弹幕内容

1.   情感分析
     -   所有弹幕的情感倾向
     -   情感趋势图
2.   关键词提取
3.   词云图

#### 4.挖掘潜在信息

1.   弹幕与视频内容之间的关联性。
2.   用户在特定事件（如视频中的某个情节）发生时的弹幕行为。
3.   用户之间的互动行为，如回复、@等。

## 三、参考

### （一）参考的代码

-   [API接口参考](https://github.com/SocialSisterYi/bilibili-API-collect)
-   [bilibili barrage analysis](https://github.com/moyuweiqing/bilibili-barrage-analysis)
-   [wordCloud](https://github.com/fuqiuai/wordCloud)
-   [popular fonts](https://github.com/chengda/popular-fonts)
-   [stop_words](https://github.com/isnowfy/snownlp/blob/fad6ae77d6c545e09fa91b8ac90bab8864c84177/snownlp/normal/stopwords.txt)

### （二）参考的方法

1.   关键词提取
     -   [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)

