import requests
from bs4 import BeautifulSoup
import iphelper
from urllib.parse import urlparse
import os


class Spider(object):

    def __init__(self, url, username, password):
        self.url = url
        self.helper = iphelper.IPPOOL(username, password)
        self.comments = []  # 储存记录的评论
        self.count = 0  # 记录统计的评论数
        self.filmname = ''
        self.get_name(url)

    def get_name(self, url):
        bs = self.safe_get(url)
        text = bs.find('h1').span.get_text()
        self.filmname = text.split(' ')[0]

    def safe_get(self, url):
        req = requests.get(url, headers=self.helper.ran_header(), proxies=self.helper.ran_proxy())
        # print(req.status_code)
        if req.status_code == 200:
            return BeautifulSoup(req.text, 'html.parser')
        else:
            print(req.status_code)
            return None

    def turn_shortcomment(self, bs):  # 在电影主页面找到短评页面
        page = bs.find('div', {'id': 'comments-section'}).find('h2').find('a')['href']
        if page:
            return page
        else:
            print('未找到相关短评！！')
            return None

    def turn_page(self, url):  # 当前页面上翻页并返回下一页
        bs = self.safe_get(url)
        if not bs:
            print('访问错误')
            return None
        next_page = bs.find('div', {'id': 'paginator'}).find('a', {'class': 'next'})
        r = urlparse(url)
        if next_page:
            print('-'*9 + '读取下一页' + '-'*9)
            ret = r.scheme + '://' + r.netloc + r.path + next_page['href']
            # print(ret)
            return ret
        else:
            print("\n没有下一页了！！！")
            return None

    def get_comments(self, url):
        bs = self.safe_get(url)
        if bs:
            comment_items = bs.find_all('span', {'class': 'short'})
            for comment in comment_items:
                self.comments.append(comment.get_text())
                self.count += 1
            print('已读取{}条评论'.format(self.count))
            return True
        else:
            return False

    def save_comments(self):
        if not os.path.exists('./comments/{}'.format(self.filmname)):
            os.mkdir('./comments/{}'.format(self.filmname))
        with open('./comments/{}/{}.txt'.format(self.filmname, self.filmname), 'w',
                  encoding='utf-8') as f:
            for comment in self.comments:
                f.write(comment)
                f.write('\n')
        print('-'*9 + '评论下载完成!!!' + '-'*9)





