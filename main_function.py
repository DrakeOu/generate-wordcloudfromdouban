from douban import Spider
import time
from cloudgen import Sheng

url = 'https://movie.douban.com/subject/25890017/'
s = Spider(url, username='', password='')
time.sleep(1)
bs = s.safe_get(s.url)
page = s.turn_shortcomment(bs)

if page:
    status = s.get_comments(page)
    while status:
        page = s.turn_page(page)
        if page:
            status = s.get_comments(page)
            time.sleep(1)
        else:
            status = False
    s.save_comments()
    cloud = Sheng(s.filmname)
    cloud.function()
