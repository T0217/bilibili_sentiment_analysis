# 导入类库
import re
import time
import warnings
import os
from os.path import join, exists
import function as fp

# 设置库中的参数
warnings.filterwarnings('ignore')


# 主函数
def main(url, segment=15, mask=False, resultpath=None):
    '''
    舆情分析主函数。

    Parameters
    ----------
    url : str
        B站的视频链接。
        例：'https://www.bilibili.com/video/BV1wq4y1s7S5/?spm_id_from=333.337.search-card.all.click&vd_source=1d24f52164a3ed510e0b7386c010cc2e'。

    segment : int, optional
        分箱的时间间隔，默认值为15。

    mask : bool, optional
        用于指定是否采用自定义背景图片。可选值为 False 和 True。
        默认值为 False，表示不采用自定义背景图片。
        如果为 True，则采用自定义背景图片。

    resultpath : str, optional
        结果保存的路径。
        例：'/home/ty/work'。

    Returns
    -------
    None.

    '''

    start_time = time.time()

    # 创建存储结果的路径
    if resultpath is None:
        resultpath = os.getcwd()
        print('The current working directory is:', resultpath)
        print('If you want to use the current path as your model_storage save path, please enter\'0\'.'
              'And if you want to use another path, please enter the path.'
              '\n', end='')
        resultpath_input = eval(input('Please enter:'))
        if resultpath_input == 0:
            resultpath = resultpath
        else:
            resultpath = resultpath_input
    else:
        resultpath = resultpath

    # 获取cid与存储结果的路径进行结合，如果不存在，则进行创建
    xml_url = fp.getXML_url_(url)
    cid = re.findall(r'com/(.*).xml', xml_url)[0]
    resultpath = join(resultpath, cid)
    if not exists(resultpath):
        os.mkdir(resultpath)

    # 获取可视化后的图片
    _ = fp.getBinVisualize_(url,
                            segment=segment,
                            save=True,
                            savepath=join(resultpath, 'bin_visualize.png'))

    # 得到弹幕数量最多的部分的评论内容和权重最高的前十个关键词
    topSegment_barrage, topSegment_keyTop_10 = fp.topSegmentBarrage_(url,
                                                                     segment=segment)

    topSegment_barrage.to_csv(join(resultpath, 'topSegment_barrage.csv'),
                              index=False)

    with open(join(resultpath, 'topSegment_key.txt'), 'w') as f:
        for word in topSegment_keyTop_10:
            f.write(f'{word}\n')

    # 得到弹幕的实际发出时间和对应的弹幕
    timeRealBarrage = fp.getBarrageTime_(xml_url,
                                         type_='Real')

    timeRealBarrage.to_csv(join(resultpath, 'timeReal_barrage.csv'),
                           index=False)

    # 情感分析
    # 所有弹幕的情感倾向
    sa_df = fp.sentiment_analyse_(url,
                                  segment=segment)
    sa_df.to_csv(join(resultpath, 'sentimentTrend.csv'),
                 index=False)

    # 情感趋势图
    fp.sentimentTrend_(url,
                       segment=segment,
                       save=True,
                       savepath=join(resultpath, 'sentimentTrend.png'))

    # 全文的关键词提取
    text_keyTop_10 = fp.topTextBarrage_(url,
                                        segment=segment)
    text_keyTop_10.to_csv(join(resultpath, 'topText_key.csv'),
                          index=False)

    # 词云图
    fp.generateWordCloud_(url,
                          segment=segment,
                          mask=mask,
                          savepath=join(resultpath, 'wordCloud.png'))

    end_time = time.time()

    print('———————————————————运行结束———————————————————')
    print('共用时 %.2f 秒' % (end_time - start_time))
