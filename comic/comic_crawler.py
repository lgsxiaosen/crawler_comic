# -*- encoding: UTF-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import requests
import os


class COMIC(object):
    """
    爬取漫画
    """
    def __init__(self):
        """初始化方法，定义一些变量"""
        self.index_page = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent }
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False


    def get_soup(self, url):
        """
        爬取网页
        :return:
        """
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')
            soup = BeautifulSoup(content)
            return soup
        except urllib.request.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

    def analyze_html(self, request_url):
        """
        解析网页，下载图片，是否翻页继续循环
        :param request_url:
        :return:
        """
        first_url = request_url + "/comic/15/2369.html"
        next_page_url = first_url
        j = 1
        while(True):
            soup = self.get_soup(next_page_url)
            # 文件名字
            title = soup.find(class_="bo_tit")
            file = title.contents[1].contents[1]
            file = file.split(">")[1].strip()
            print(file)
            document_name = "/"+file+"/"
            script_list = soup.find_all("script")
            for scrip in script_list:
                scrip_string = scrip.string
                if scrip_string is not None and "https://img.yaoyaoliao.com/" in scrip_string:
                    # print(scrip_string)
                    # 循环下载图片
                    print("下载第：{}章".format(j))
                    pic_url_or = scrip_string.split(";")
                    prefix_url = pic_url_or[0].split("'")[1]
                    # print(prefix_url)
                    url_string_list = pic_url_or[1].split("'")[1]
                    url_string_list = url_string_list.replace("\\", "")
                    pic_url_list = eval(url_string_list)
                    # print(pic_url_list)
                    # 遍历下载图片
                    i = 1
                    for pic_url in pic_url_list:
                        file_name = str(i) + ".jpg"
                        download_url = prefix_url + pic_url
                        self.download_pic(download_url, file_name, document_name)
                        print("第：{}章，第：{}张图片下载完成！".format(j, i))
                        i += 1
                    print("下载完成第：{}章，共：{}张图片！".format(j, i))
                    break
            # 下一页
            next_page = self.get_next_page(soup)
            if next_page is None or first_url==(request_url + next_page):
                break
            next_page_url = request_url + next_page
            j += 1
            # if j>=4:
            #     break



    def get_next_page(self, soup):
        """
        获取下一页的url，没有下一页返回None
        :param soup:
        :return:
        """
        next = soup.find(class_="bo_nav").find_all()
        for n in next:
            if "id" in n.attrs and n.attrs["id"] == "xurl":
                next_url = n.attrs["href"]
                print(next_url)
                return next_url
        return None

    def download_pic(self, pic_url, file_name, doucument_name):
        """
        下载图片
        :param pic_url:
        :return:
        """
        dir = os.getcwd()
        download_file_name = dir+'/pic'+doucument_name
        if not os.path.exists(download_file_name):
            os.makedirs(download_file_name)
        r = requests.get(pic_url, stream=True)
        # print(r.status_code)  # 返回状态码
        if r.status_code == 200:
            open(dir+'/pic'+doucument_name+file_name, 'wb').write(r.content)  # 将内容写入图片
            # print("done")
        del r


if __name__ == '__main__':
    comic = COMIC()
    comic.analyze_html("https://m.bnmanhua.com")
    # s = """
    # var z_img='["images\/comic\/159\/316518\/1519527843Efo9qfJOY9Jb_VP4.jpg","images\/comic\/159\/316518\/1519527844GMfoVznVXkoEWSLN.jpg","images\/comic\/159\/316518\/1519527844fIPxE1l7oRlFRjd-.jpg","images\/comic\/159\/316518\/1519527845mjhIqfGEIN0tRiq9.jpg","images\/comic\/159\/316518\/1519527845bO68qo1r4N0X8Hfr.jpg","images\/comic\/159\/316518\/1519527845-fYNeLkaFcGP38i-.jpg","images\/comic\/159\/316518\/1519527846tgV0x-wAkDEahA3k.jpg","images\/comic\/159\/316518\/1519527846p5uRD0AUBh7VAck5.jpg","images\/comic\/159\/316518\/15195278469Y6xh_jqDJObWelu.jpg","images\/comic\/159\/316518\/1519527847txbRWVPoMcWbh1TS.jpg","images\/comic\/159\/316518\/1519527847DTU5whH2NtlfY7v4.jpg","images\/comic\/159\/316518\/1519527848ZltMhw4VMGzQ9L_z.jpg","images\/comic\/159\/316518\/1519527848dTGU46MD9w4zeeD2.jpg","images\/comic\/159\/316518\/1519527848CsevgzpNn_8SfML9.jpg","images\/comic\/159\/316518\/1519527849IWDG-ZjBecRW0wbN.jpg","images\/comic\/159\/316518\/1519527849YF7JdQQOaWdsCP4d.jpg","images\/comic\/159\/316518\/1519527849eYMmWKilAcCz_Dhs.jpg","images\/comic\/159\/316518\/1519527850Nbkg49URJs8DRwqC.jpg"]'
    # """
    # a = s.split("'")[1]
    # a = eval(a)
    # print(a)