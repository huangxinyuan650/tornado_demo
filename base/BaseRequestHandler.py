# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/15 16:23
# File: BaseRequestHandler.py
from typing import Optional, Awaitable
import logging

from tornado.web import RequestHandler


class BaseRequestHandler(RequestHandler):

    def initialize(self, **kwargs):
        """
        设置Handler初始化时接收注入的属性（db等）
        :param kwargs:
        :return:
        """
        [setattr(self, _k, _v) for _k, _v in kwargs.items()]

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self) -> Optional[Awaitable[None]]:
        """
        在调用http方法之前调用，增加统一处理
        若此方法调用finish方法或者redirect，处理会在这里终止
        :return:
        """
        logging.info(f'{self.request.method} Request from {self.request.host_name}:{self.request.uri}')

    def on_finish(self) -> None:
        """
        请求处理完成后调用的方法，同步请求时在http方法执行完后即执行，异步处理时在finish方法执行完后执行
        :return:
        """
        logging.info(f'{self.request.method} Request from {self.request.host_name} has been handled!!!')

    def set_default_headers(self) -> None:
        """
        设置响应时附加的header
        :return:
        """
        self.set_cookie('tornado_token', '111111')
        self.add_header('tornado', 'yes')
