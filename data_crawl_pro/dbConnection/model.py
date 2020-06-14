from sqlalchemy import Column, String, Integer, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class JsonData(Base):
    __tablename__ = 'jsondata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200),nullable=False)
    model = Column(JSON, nullable=False)
    data = Column(Text)
    picture = Column(Text)
    registerTime = Column(DateTime(timezone=True), default=datetime.now)
    latestModifyTime = Column(DateTime(timezone=True), default=datetime.now)
