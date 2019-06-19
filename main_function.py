from body import Spider
import time
from cloudgen import Sheng

s = Spider(url='xxx', username='xxx', password='xxx')
page = s.find_shortcomment()

if page:
    s.get_comments(page)
    s.save_comments()
    cloud = Sheng(s.filmname)   # 使用pictures文件夹中的随机图片生成矩阵
    cloud.function()
