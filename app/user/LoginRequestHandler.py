# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 22:44
# File: LoginRequestHandler.py

from base.BaseRequestHandler import BaseRequestHandler
from utils import HandlerRouter
from app.user.LoginService import LoginService


@HandlerRouter(path='/login')
class LoginRequestHandler(BaseRequestHandler):
    """
    登录请求处理handler
    """

    def get(self):
        # Get 请求跳转登录页
        self.render('login.html')

    def post(self, *xargs, **kwargs):
        """
        post 登录验证
        验证成功跳转至主页，失败继续跳转至登录页
        :param xargs:
        :param kwargs:
        :return:
        """
        _login_svc = LoginService(self.request)
        if _login_svc.login(user_name=self.get_argument('user_name'),password=self.get_argument('password')):
            self.render('index.html', info_list=['a', 'b', 'c', 'd'])
        else:
            self.render('login.html')
