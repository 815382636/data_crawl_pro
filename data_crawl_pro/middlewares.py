# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from browsermobproxy import Server
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http.response.html import HtmlResponse


class DataCrawlProDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # 下载地址：http://chromedriver.storage.googleapis.com/index.html
    #服务器版本：83.0.4103.106-1
    def __init__(self):
        server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy",options={'port':8091})
        server.start()
        self.proxy = server.create_proxy()

        # 加载测试浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_driver = r'./chromedriver'
        self.driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        self.driver.implicitly_wait(120)


    # 返回request：则scrapy会去服务器加载资源
    # 返回response：则跳过资源下载直接交给解析方法
    def process_response(self, request, response, spider):
        # 模拟人类行为
        self.proxy.new_har(request.url)
        self.driver.get(request.url)
        time.sleep(30)
        result = self.proxy.har
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            if _url not in spider.urls:
                spider.urls.append(_url)
        source = self.driver.page_source
        # 创建一个response对象,把页面信息封装在response对象中
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding="utf-8")
        return response

