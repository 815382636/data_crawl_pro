# -*- coding: utf-8 -*-
import scrapy
from lxml.html import tostring
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
import json
import requests
from data_crawl_pro.items import DataCrawlProItem


class DataSpiderSpider(CrawlSpider):
    name = 'data_spider'
    # allowed_domains = ['vega.github.io']
    start_urls = ['https://vega.github.io']
    rules = (
        Rule(LinkExtractor(
            allow=[r'https://vega.github.io/.*', r'https://bl.ocks.org/.*', r'https://makingdatavisual.github.io/.*']),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        if "https://makingdatavisual.github.io" in response.url:
            if response.selector.xpath("//*[@class='vega-embed']"):
                data_url = "https://makingdatavisual.github.io/spec/" + response.url.split("/")[-1] + ".vl.json"
                res = requests.get(data_url)
                item = DataCrawlProItem()
                item["data"] = json.loads(res.text)
                item["url"] = response.url
                item["name"] = response.selector.xpath('//h2/text()').extract_first()
                item["picture"] = response.selector.xpath("//*[name()='svg' and @class ='marks']").extract_first()
                yield item


        else:
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
                        item["picture"] = response.selector.xpath(
                            "//*[name()='svg' and @class ='marks']").extract_first()
                        yield item
