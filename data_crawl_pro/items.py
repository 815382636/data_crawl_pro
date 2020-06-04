# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#模型类，插入数据库
class DataCrawlProItem(scrapy.Item):
    # define the fields for your item here like:
    url = data = name = picture = scrapy.Field()
