# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
import requests
from data_crawl_pro.items import DataCrawlProItem


def test_exist(list, data):
    for i in list:
        if data == i["model"]:
            return True
    return False


class DataSpiderSpider(CrawlSpider):
    name = 'data_spider'
    # allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io/vega-lite/examples/bar.html']
    rules = (
        Rule(LinkExtractor(
            allow=[r'https://vega.github.io/.*', r'https://bl.ocks.org/.*', r'https://makingdatavisual.github.io/.*']),
            callback='parse_item', follow=True),
    )

    def __init__(self):
        super().__init__()
        self.urls = []

    def parse_item(self, response):

        # 获取model  1.通过network获取 2.通过网页内容获取
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
                    data_model = {}
                    data_model["model"] = json_data
                    data_model["url"] = response.url
                    # 获取图片
                    data_model["picture"] = response.selector.xpath(
                        "//*[name()='svg' and @class ='marks']").extract_first()

                    # 将data_model加入item
                    if item.get("model_list"):
                        if not test_exist(item.get("model_list"), json_data):
                            item["model_list"].append(data_model)
                    else:
                        item["model_list"] = [data_model]

        # 通过network获取
        for url in self.urls:
            if "vl.json" in url:
                res = requests.get(url)
                data_model = {}
                data_model["model"] = json.loads(res.text)
                data_model["url"] = response.url
                # 获取图片
                data_model["picture"] = response.selector.xpath("//*[name()='svg' and @class ='marks']").extract_first()
                if item.get("model_list"):
                    if not test_exist(item["model_list"], data_model["model"]):
                        item["model_list"].append(item)
                else:
                    item["model_list"] = [data_model]

        # 获取model中的数据
        if item.get("model_list"):
            for i in item["model_list"]:
                if "data" in i["model"].keys():
                    if "url" in i["model"]["data"].keys():
                        data_url = i["model"]["data"]["url"]
                        if "https://" in data_url:
                            data_res = requests.get(data_url).text
                            i["data"] = data_res
                        else:
                            for url in self.urls:
                                if data_url in url:
                                    data_res = requests.get(url).text
                                    i["data"] = data_res

        yield item
