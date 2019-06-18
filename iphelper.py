import requests
import time
import random
import os


class IPPOOL(object):

    def __init__(self, username, password):
        self.params = dict()
        self.cookies = list()
        self.proxies = ['122.193.245.5', '112.85.128.161', '27.43.191.175', '163.204.241.224', '163.204.243.137',
                        '125.123.128.104', '121.69.46.177', '222.223.182.660', '1.197.203.16']
        self.useragent = ['Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,lik'
                          'eGecko)Version/5.1Safari/534.50',
                          'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)'
                          'Version/5.1Safari/534.50',
                          'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
                          'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
                          'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
                          'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.X'
                          'MetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
                          'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)'
                          ]
        self.params['username'] = username
        self.params['password'] = password
        self.get_cookies()

    def clear_cookie(self):
        if os.path.exists('cookies.txt'):
            os.remove('cookies.txt')
            print('已清空cookie！！！')
        else:
            print('不存在已下载cookie!!!')

    def get_cookies(self, url='http://www.douban.com/'):
        if os.path.exists('cookies.txt'):
            with open('cookies.txt', 'r', encoding='utf-8') as fb:
                line = fb.readline().strip('\n')

                while line:
                    self.cookies.append(str(line))
                    line = fb.readline().strip('\n')
            print('已有cookies')
        else:
            for i in range(10):     # 登陆10次获取cookie
                try:
                    req = requests.post(url, self.params)
                except requests.exceptions.RequestException:
                    break
                self.cookies.append(req.cookies.get_dict()['bid'])
                print('-'*9 + '正在获取第{}条cookie!'.format(i+1) + '-'*9)
                time.sleep(1)
            with open('.\cookies.txt', 'w', encoding='utf-8') as f:
                for cookie in self.cookies:
                    f.write(cookie)
                    f.write('\n')

    def ran_header(self):
        header = dict()
        header['User-Agent'] = random.choice(self.useragent)
        header['Cookie'] = 'bid={}; ll="118254"; _vwo_uuid_v2=DE7F302B9F032B393DF1E7E' \
                           '6578105CAB|ba3c68f1ed794d2b800f0f2c441c6d47; gr_user_id=e835fd71-3' \
                           '740-43e2-a973-f5cac6520d0f; push_doumail_num=0; push_noty_num=0; _' \
                           '_gads=ID=54b9eac113427c9d:T=1559958778:S=ALNI_MZWC6WrFzuo_FEa4Fbvq' \
                           'Hl2j8isjw; trc_cookie_storage=taboola%2520global%253Auser-id%3D815' \
                           '43f66-ef55-4ca8-9d8d-98107ba79f90-tuct3ed5bad; ct=y; __yadk_uid=xV' \
                           'CucQMv4wgF7DVZy2NC4qCUPt5TYqCM; __utmv=30149280.5020; douban-fav-r' \
                           'emind=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1560763336%2C%22' \
                           'https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.8cb4=b59c5aa935f' \
                           '9325c.1558245712.12.1560763336.1560752043.; _pk_ses.100001.8cb4=*;' \
                           ' __utma=30149280.333222740.1559958854.1560751613.1560763338.13; __' \
                           'utmc=30149280; __utmz=30149280.1560763338.13.10.utmcsr=cn.bing.com' \
                           '|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=3014' \
                           '9280.1.10.1560763338; dbcl2="50202526:6iyOkYrnuQM"'.format(random.choice(self.cookies))
        return header

    def ran_proxy(self):
        for i in range(10):
            ip = dict()
            ip['http'] = 'http://' + random.choice(self.proxies)
            req = requests.get('https://www.baidu.com/', proxies=ip)    # 访问百度测试代理是否可用
            if req.status_code == 200:
                return ip
        print('全部ip已不可用！！！')
        # 从代理池中重新爬取ip


