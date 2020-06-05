# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
import json
from data_crawl_pro.items import DataCrawlProItem


class DataSpiderSpider(CrawlSpider):
    name = 'data_spider'
    allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io/']
    rules = (
        Rule(LinkExtractor(allow=r'https://vega.github.io/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        html = etree.HTML(response.text)
        code_list = html.xpath("//code[contains(@class,'language-json')]/text()")
        if len(code_list) != 0:
            for i in code_list:
                json_data = json.loads(i)
                if '$schema' in json_data.keys():
                    if json_data['$schema'] == 'https://vega.github.io/schema/vega-lite/v4.json':
                        # 模型赋值
                        item = DataCrawlProItem()
                        item["data"] = json_data
                        item["url"] = response.url
                        name = html.xpath("//div[contains(@class,'page-centered')]/h1/text()")
                        if len(name) != 0:
                            item["name"] = name[0]
                        # picture =html.xpath("//svg[contains()@class,'marks']/attribute::*")
                        # if len(picture) !=0:
                        #     item["picture"] =picture

                        yield item
