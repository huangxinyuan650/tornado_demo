# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 21:59
# File: UserRequestHandler.py
from base.BaseRequestHandler import BaseRequestHandler
from utils import HandlerRouter


@HandlerRouter(path='/user')
class UserRequestHandler(BaseRequestHandler):
    """
    用户请求处理handler
    """
