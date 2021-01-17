# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/15 16:39
# File: TestDemoRequestHandler.py
from base.BaseRequestHandler import BaseRequestHandler
from utils import HandlerRouter
import tornado


@HandlerRouter(path='/(wengen|model)/test')
class TestDemoRequestHandler(BaseRequestHandler):

    @tornado.gen.coroutine
    def get(self, *xargs, **kwargs):
        print(xargs)
        print(kwargs)
        yield
        # self.write(f'{self.on_response()}')
        self.render('index.html', info_list=['a', 'b', 'c'])

    def on_response(self):
        return 'hxy'


@HandlerRouter(path='/(test|ceshi)/test')
class DemoRequestHandler(BaseRequestHandler):

    def get(self, *xargs, **kwargs):
        print(xargs)
        print(kwargs)
        self.render('index.html', info_list=['a', 'b', 'c', 'd', 'e', 'f'])
