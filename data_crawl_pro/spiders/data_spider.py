# -*- coding: utf-8 -*-
import scrapy
from lxml.html import tostring
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
import json
from data_crawl_pro.items import DataCrawlProItem


class DataSpiderSpider(CrawlSpider):
    name = 'data_spider'
    allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io/vega-lite/examples/bar.html']
    rules = (
        Rule(LinkExtractor(allow=r'https://vega.github.io/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        html = etree.HTML(response.text)
        code_list = html.xpath("//code[contains(@class,'language-json')]/descendant-or-self::text()")
        if len(code_list) != 0:
            str = ''.join(code_list)
            json_data = json.loads(str)
            if '$schema' in json_data.keys():
                if json_data['$schema'] == 'https://vega.github.io/schema/vega-lite/v4.json':
                    # 模型赋值
                    item = DataCrawlProItem()
                    item["data"] = json_data
                    item["url"] = response.url
                    name = html.xpath("//div[contains(@class,'page-centered')]/h1/text()")
                    if len(name) != 0:
                        item["name"] = name[0]
                    picture = html.xpath("//*[name()='svg']")
                    if len(picture) != 0:
                        item["picture"] = tostring(picture[0], encoding="utf-8").decode("utf-8")

                    yield item
