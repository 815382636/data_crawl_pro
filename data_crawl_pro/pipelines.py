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
        jsonData = JsonData(url=item.get("url"), data=item.get("data"), name=item.get("name"),
                            picture=item.get("picture"))
        try:
            self.session.add(jsonData)
            self.session.commit()
        except:
            self.session.rollback()
        return item
