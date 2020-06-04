# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import MetaData

from data_crawl_pro.dbConnection.pg_connection import connection
from data_crawl_pro.dbConnection.model import JsonData,Base

class DataCrawlProPipeline(object):

    def __init__(self):
        self.session,engine =connection()
        metadata = MetaData(engine)
        tables = metadata.tables
        if "jsondata" not in tables:
            Base.metadata.create_all(engine)


    def process_item(self, item, spider):

        # print(item)
        jsonData =JsonData(url =item.get("url"),data =item.get("data"),name =item.get("name"),picture=item.get("picture"))
        # print(jsonData.id,jsonData.registerTime,jsonData.url)
        try:
            self.session.add(jsonData)
            self.session.commit()
        except :
            self.session.rollback()

        return item
