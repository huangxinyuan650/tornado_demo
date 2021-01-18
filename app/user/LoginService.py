# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 23:54
# File: LoginService.py
from base.BaseService import BaseService
from app.user.UserModel import UserInfo, RoleBinding
import uuid


class LoginService(BaseService):

    def login(self, user_name, password):
        """
        获取登录信息
        :param user_name:
        :param password:
        :return:
        """
        _list = self.utils.db.read.query(UserInfo.id) \
            .join(RoleBinding, UserInfo.id == RoleBinding.user_id) \
            .filter(UserInfo.user_name == user_name) \
            .filter(UserInfo.authorize_string == password).all()
        _token = uuid.uuid4() if _list else None
