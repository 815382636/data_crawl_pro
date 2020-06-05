from sqlalchemy import Column, String, Integer, JSON, DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class JsonData(Base):
    __tablename__ = 'jsondata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), unique=True, nullable=False)
    data = Column(JSON, nullable=False)
    name = Column(String(200))
    picture = Column(Text)
    registerTime = Column(DateTime(timezone=True), default=datetime.now)
    latestModifyTime = Column(DateTime(timezone=True), default=datetime.now)
