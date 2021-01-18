# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/18 09:36
# File: auto_update_db.py

from utils import util_objet, import_handler
from base.BaseModel import Base

if __name__ == '__main__':
    import_handler(module_list=[_a for _, _a in util_objet.config.get_conf(_section='app')], endswith='Model.py')
    Base.metadata.create_all(util_objet.db.db_engine)
