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
    # allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io']
    rules = (
        Rule(LinkExtractor(allow=[r'https://vega.github.io/.*',r'https://bl.ocks.org/.*']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # html = etree.HTML(response.text)
        # code_list = html.xpath("//code[contains(@class,'language-json')]/descendant-or-self::text()")
        # if len(code_list) != 0:
        #     str = ''.join(code_list)
        #     json_data = json.loads(str)
        #     if '$schema' in json_data.keys():
        #         if json_data['$schema'] == 'https://vega.github.io/schema/vega-lite/v4.json':
        #             # 模型赋值
        #             item = DataCrawlProItem()
        #             item["data"] = json_data
        #             item["url"] = response.url
        #             name = html.xpath("//div[contains(@class,'page-centered')]/h1/text()")
        #             if len(name) != 0:
        #                 item["name"] = name[0]
        #             picture = html.xpath("//*[name()='svg']")
        #             if len(picture) != 0:
        #                 item["picture"] = tostring(picture[0], encoding="utf-8").decode("utf-8")
        result = response.selector.xpath('//*')
        for i in result:
            elements = i.xpath("./*/text()").extract()
            if '''"$schema"''' in elements and (
                    '''"https://vega.github.io/schema/vega-lite/v2.json"''' in elements or '''"https://vega.github.io/schema/vega-lite/v4.json"''' in elements):
                code_list = i.xpath("./descendant-or-self::text()").extract()
                if code_list:
                    str = ''.join(code_list)
                    json_data = json.loads(str)
                    item = DataCrawlProItem()
                    item["data"] = json_data
                    item["url"] = response.url
                    item["name"] = response.selector.xpath('//h1/text()').extract_first()
                    item["picture"] = response.selector.xpath("//*[name()='svg' and @class ='marks']").extract_first()
                    print(item)
                    yield item
