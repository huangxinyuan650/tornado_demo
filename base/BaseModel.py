# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 12:07
# File: BaseModel.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from utils import util_objet

Base = declarative_base()


class BaseModel(Base):
    id = Column(Integer)
    short_desc = Column(String(20))

    @classmethod
    def db(cls):
        return util_objet.db.write

    @classmethod
    def redis(cls):
        return util_objet.redis
