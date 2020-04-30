# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    gsliu 2017-03-03
    
"""
import re
import urllib.request

from bs4 import BeautifulSoup

page = 1
url = 'http://www.qiushibaike.com/hot/8hr/page/' + str(page)
if page > 1:
    url = url + '/?s=4961777'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # # content = content.replace('<br/>', '\n')
    # pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?'
    #                      '<div class="content">.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>', re.S)
    # items = re.findall(pattern, content)
    # for item in items:
    #     rep = re.compile('<br/>')
    #     text = re.sub(rep, '\n', item[1])
    #     print(item[0] + ':', '\n', text, '\n', u'点赞：' + item[2], '\n')
    soup = BeautifulSoup(content)

    authors = soup.find_all(class_="article block untagged mb15")
    for authou in authors:
        main = authou.find(class_="content")
        if main.span.string is None:
            continue
        print('名字：', authou.h2.string)
        print('内容：', main.span.string)
        number = authou.find(class_="number")
        print('点赞数：', number.string)
        print('')

except urllib.request.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)
