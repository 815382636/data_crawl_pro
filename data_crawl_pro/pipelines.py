# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import MetaData

from data_crawl_pro.dbConnection.pg_connection import connection
from data_crawl_pro.dbConnection.model import JsonData, Base
import hashlib
import json


class DataCrawlProPipeline(object):

    def __init__(self):
        self.session, engine = connection()
        metadata = MetaData(engine)
        tables = metadata.tables
        if "jsondata" not in tables:
            Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        if item:
            model_to_hash = item.get("model")
            model_to_hash = json.dumps(model_to_hash)
            model_to_hash = str(uuid.uuid3(uuid.NAMESPACE_DNS, model_to_hash))
            jsonData = JsonData(url=item.get("url"), data=item.get("data"), model=item.get("model"),
                                picture=item.get("picture"), hashmodel=model_to_hash)
            try:
                self.session.add(jsonData)
                self.session.commit()
            except:
                self.session.rollback()
        return item
