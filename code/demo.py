# 导入类库
from main import main

# 设置B站的视频链接和结果存储路径
url1 = 'https://www.bilibili.com/video/BV1wq4y1s7S5/?spm_id_from=333.337.search-card.all.click&vd_source=1d24f52164a3ed510e0b7386c010cc2e'

resultpath = r"C:\Users\18840\Desktop"

# 运行主函数
main(url1, segment=15, mask=False, resultpath=resultpath)
