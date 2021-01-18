# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/18 10:47
# File: RedisService.py

from utils import util_objet


class RedisService(object):

    @staticmethod
    def set_key(key: str, value: str, expires: int = None):
        """
        Redis设置str值操作，默认无过期时间
        :param key:
        :param value:
        :param expires:
        :return:
        """
        return util_objet.redis.set(name=key, value=value, ex=expires)

    @staticmethod
    def set_key_expires(key: str, expires: int):
        """
        为某个key设置过期时间
        :param key:
        :param expires:
        :return:
        """
        return util_objet.redis.pexpire(name=key, time=expires)

    @staticmethod
    def set_key_nx(key: str, value: str):
        """
        设置key、value，原子操作，不存在则设置完成并返回1，存在返回0，可做分布式锁
        :param key:
        :param value:
        :return:
        """
        return util_objet.redis.setnx(name=key, value=value)

    @staticmethod
    def get_redis_obj():
        """
        针对一些极端情况需要拿到redis的控制权，则直接返回redis对象
        :return:
        """
        return util_objet.redis
