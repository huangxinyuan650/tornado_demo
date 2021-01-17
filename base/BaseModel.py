# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 12:07
# File: BaseModel.py

from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, String
from utils import util_objet

class_registry = {}
Base = declarative_base(class_registry=class_registry)


class BaseModel(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    short_desc = Column(String(20))

    @classmethod
    def db(cls):
        return util_objet.db.write

    @classmethod
    def redis(cls):
        return util_objet.redis
