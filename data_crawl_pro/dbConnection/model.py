from sqlalchemy import Column,String,Integer,JSON,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class JsonData(Base):

    __tablename__ = 'jsondata'

    id = Column(Integer, primary_key=True,autoincrement=True,default=1)
    url = Column(String(50),unique=True, nullable=False)
    data =Column(JSON,nullable=False)
    name =Column(String(50))
    picture =Column(String(200))
    registerTime =Column(DateTime(timezone=True), default=datetime.now)
    latestModifyTime =Column(DateTime(timezone=True), default=datetime.now)


