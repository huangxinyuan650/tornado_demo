# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 23:54
# File: BaseService.py

from utils import util_objet


class BaseService(object):
    """
    服务类基类，请求进入handler后将直接交由Service类进行实际的业务处理
    """

    def __init__(self, request: object = None):
        self.request = request
        self._utils = util_objet
        self.initialize()

    def initialize(self):
        """
        服务初始化，待实现
        :return:
        """
        pass
