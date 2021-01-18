# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 12:18
# File: UserModel.py
from base.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import enum

"""
用户基本信息表（UserInfo），与角色表（RoleInfo）的关系为绑定表（RoleBinding）
"""


class UserInfo(BaseModel):
    __tablename__ = 'user_info'

    user_name = Column(String(40), nullable=False, doc='User Name')
    mobile = Column(String(11), doc='Mobile')
    authorize_string = Column(String(20), doc='PassWord which has been encrypted')


"""
角色表，与用户信息表的关系为绑定表
"""


class RoleType(enum.Enum):
    """
    模拟linux文件系统权限，初始为READ、WRITE、MANAGE（X）依次升级，且可在中间插入其他权限
    """
    READ = 1
    WRITE = 10
    MANAGE = 20


class RoleInfo(BaseModel):
    __tablename__ = 'role_info'

    role_name = Column(String(20), nullable=False, doc='Role Name')
    role_desc = Column(String(40))
    role_type = Column(Enum(RoleType), doc='{1:READ,10:WRITE,20:MANAGE}')
    role_range = Column(Integer)


"""
关系绑定表
"""


class RoleBinding(BaseModel):
    __tablename__ = 'role_binding'

    user_id = Column(Integer, ForeignKey('user_info.id'), doc='关联用户信息表')
    role_info = Column(Integer, ForeignKey('role_info.id'), doc='关联权限信息表')
    manage_range = Column(Integer, doc='权限范围')
