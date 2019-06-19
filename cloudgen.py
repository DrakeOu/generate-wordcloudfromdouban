import jieba.analyse
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import random


class Sheng(object):
    def __init__(self, filename):
        self.filename = filename                              # 获取文件名
        self.image = Image.open('./pictures/{}'.format(self.get_image()))       # 打开图片

    def get_image(self):
        path = './pictures'
        files = os.listdir(path)
        return random.choice(files)

    def get_font(self):
        path = './font'
        fonts = os.listdir(path)
        return fonts[0]

    def get_content(self, filename):
        content = ''
        with open('./comments/{}/{}.txt'.format(filename, filename), 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                content += line
                line = f.readline()
        return content

    def function(self):
        graph = np.array(self.image)  # 获取矩形
        wc = WordCloud(font_path='./font/{}'.format(self.get_font()), background_color='White', max_words=50, mask=graph)
        # 字体路径，背景颜色，最大数量，选用背景矩阵
        content = self.get_content(self.filename)
        result = jieba.analyse.textrank(content, topK=50, withWeight=True)
        keywords = dict()
        for i in result:
            keywords[i[0]] = i[1]

        wc.generate_from_frequencies(keywords)
        image_color = ImageColorGenerator(graph)
        plt.imshow(wc)
        plt.imshow(wc.recolor(color_func=image_color))
        plt.axis("off")
        if not os.path.exists('./ciyun'):
            os.mkdir('./ciyun')
        wc.to_file('./ciyun/{}.png'.format(self.filename, self.filename))
        print('已生成词云-----{}'.format(self.filename))

