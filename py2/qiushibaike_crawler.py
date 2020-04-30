# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    gsliu 2017-03-06
    
"""
import re
import urllib.request


class QSBK():
    """糗事百科爬虫"""
    def __init__(self):
        """初始化方法，定义一些变量"""
        self.Indexpage = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent }
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    def getPage(self, Indexpage):
        """传入某一页的索引获得页面代码"""
        try:
            url = 'http://www.qiushibaike.com/hot/8hr/page/' + str(Indexpage)
            if Indexpage > 1:
                url = url + '/?s=4961777'
            # 构建请求的request
            request = urllib.request.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib.request.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            # pageCode = pageCode.replace('<br/>', '\n')
            return pageCode
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接糗事百科失败,错误原因", e.reason)
                return None

    def getPageItems(self,pageIndex):
        """传入某一页代码，返回本页不带图片的段子列表"""
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?'
                             '<div class="content">.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储每页的段子们
        pageStories = []
        # 遍历正则表达式匹配的信息
        for item in items:
            rep = re.compile('<br/>')
            text = re.sub(rep, '\n', item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        return pageStories

    def loadPage(self):
        """加载并提取页面的内容，加入到列表中"""
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable:
            if len(self.stories) < 2:
                # 获取新一页
                pageStories = self.getPageItems(self.Indexpage)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.Indexpage += 1

                    # 调用该方法，每次敲回车打印输出一个段子

    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print(u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story[0], story[2], story[1]))

    def start(self):
        # 开始方法
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()
