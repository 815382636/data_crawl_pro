# -*- coding: utf-8 -*-

from sqlalchemy import MetaData

from data_crawl_pro.dbConnection.pg_connection import connection
from data_crawl_pro.dbConnection.model import JsonData, Base


class DataCrawlProPipeline(object):

    def __init__(self):
        self.session, engine = connection()
        metadata = MetaData(engine)
        tables = metadata.tables
        if "jsondata" not in tables:
            Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        if item.get("model_list"):
            for i in item["model_list"]:
                jsonData = JsonData(url=i.get("url"), data=i.get("data"), model=i.get("model"),
                                    picture=i.get("picture"))
                try:
                    self.session.add(jsonData)
                    self.session.commit()
                except:
                    self.session.rollback()
        return item
