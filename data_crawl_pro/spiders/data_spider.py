# -*- coding: utf-8 -*-
import csv

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
import requests
from data_crawl_pro.items import DataCrawlProItem


class DataSpiderSpider(CrawlSpider):
    name = 'data_spider'
    # allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io/']
    rules = (
        Rule(LinkExtractor(
            allow=[r'https://vega.github.io/.*', r'https://bl.ocks.org/.*', r'https://makingdatavisual.github.io/.*',r'https://www.trafforddatalab.io/.*',r'https://observablehq.com/.*']),
            callback='parse_item', follow=True),
    )

    def __init__(self):
        super().__init__()
        self.urls = []

    def parse_item(self, response):
        # 将爬取的网页写入txt
        with open("./through_urls.txt", "a") as file:
            file.write(response.url + "\n")
            file.close()

        # 拿到proxy中的network的url
        network_url = self.urls
        self.urls = []

        # 获取model  1.通过network获取 2.通过网页内容获取 3.通过点击获取（缺地球情况）
        item = DataCrawlProItem()
        # 通过网页内容获取
        result = response.selector.xpath('//*')
        for i in result:
            elements = i.xpath("./*/text()").extract()

            type = False
            for element in elements:
                if '''"https://vega.github.io/schema/vega-lite/''' in element:
                    type = True
            if '''"$schema"''' in elements and type:
                code_list = i.xpath("./descendant-or-self::text()").extract()
                if code_list:
                    str = ''.join(code_list)
                    json_data = json.loads(str)
                    item["model"] = json_data
                    item["url"] = response.url
                    item["picture"] = response.selector.xpath(
                        "//*[name()='svg' and @class ='marks']").extract_first()
                    get_data(item, network_url)

                    yield item

        # 通过network获取
        if not item:
            for url in network_url:
                if "vl.json" in url:
                    res = requests.get(url)
                    item["model"] = json.loads(res.text)
                    item["url"] = response.url
                    item["picture"] = response.selector.xpath(
                        "//*[name()='svg' and @class ='marks']").extract_first()
                    get_data(item, network_url)
                    yield item

        # 爬取代码不合适
        vega_actions = response.selector.xpath("//*[@class ='vega-actions']")
        if vega_actions and not item:
            with open('./error_urls.txt', 'a') as file:
                file.write(response.url + "\n")
                file.close()

        yield item


def get_data(item, network_url):
    if item.get("model") and "data" in item["model"].keys():
        if "url" in item["model"]["data"].keys():
            data_url = item["model"]["data"]["url"]
            data_res = ''
            if "https://" in data_url:
                data_res = requests.get(data_url).text
            else:
                for url in network_url:
                    if data_url in url:
                        data_url = url
                        data_res = requests.get(url).text
            if 'json' in data_url:
                new_data = json.loads(data_res)
                di = {}
                di[data_url] = new_data
                item["data"] = di
            elif 'csv' in data_url:
                new_data = list(csv.reader(data_res.split('\n'), delimiter=','))
                di = {}
                di[data_url] = new_data
                item["data"] = di
            else:
                new_data = data_res
                di = {}
                di[data_url] = new_data
                item["data"] = di
