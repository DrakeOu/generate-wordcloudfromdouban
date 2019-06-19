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
        self.filmname = text.split(' ')[0]  # 选取中文名

    def safe_get(self, url):
        resp = requests.get(url, headers=self.helper.ran_header(), proxies=self.helper.ran_proxy())
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, 'html.parser')
        else:
            print('{}错误!!!'.format(resp.status_code))
            return None

    def find_shortcomment(self):  # 在电影主页面找到短评页面
        bs = self.safe_get(self.url)
        if not bs:
            return None
        page = bs.find('div', {'id': 'comments-section'}).find('h2').find('a')['href']
        if page:
            return page
        else:
            print('未找到相关短评!!请检查标签')
            return None

    def turn_page(self, url):  # 当前页面上翻页并返回下一页
        bs = self.safe_get(url)
        if not bs:
            return None
        next_page = bs.find('div', {'id': 'paginator'}).find('a', {'class': 'next'})
        r = urlparse(url)
        if next_page:
            print('-'*9 + '读取下一页' + '-'*9)
            ret = r.scheme+'://'+r.netloc+r.path+next_page['href']
            return ret
        else:
            print("\n没有下一页了!!!")
            return None

    def get_comments(self, page_url):
        while page_url:
            bs = self.safe_get(page_url)
            if not bs:
                break
            comment_items = bs.find_all('span', {'class': 'short'})
            for comment in comment_items:
                self.comments.append(comment.get_text())
                self.count += 1
            print('已读取{}条评论'.format(self.count))
            page_url = self.turn_page(page_url)

    def save_comments(self):
        if not os.path.exists('./comments'):
            os.mkdir('./comments')
        if not os.path.exists('./comments/{}'.format(self.filmname)):
            os.mkdir('./comments/{}'.format(self.filmname))
        with open('./comments/{}/{}.txt'.format(self.filmname, self.filmname), 'w',
                  encoding='utf-8') as f:
            for comment in self.comments:
                f.write(comment)
                f.write('\n')
        print('-'*9 + '评论下载完成!!!' + '-'*9)





