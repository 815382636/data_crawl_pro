from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from data_crawl_pro.properties import SQLALCHEMY_DATABASE_URI


def connection():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    metadata = MetaData(engine)
    tables = metadata.tables
    print(tables)
    return session, engine
