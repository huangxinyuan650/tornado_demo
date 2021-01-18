# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/17 11:24
# File: utils.py

import configparser
import os
from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis import StrictRedis, ConnectionPool
from rediscluster import RedisCluster
import importlib

"""
工具集合
1、配置文件
"""
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 3


def import_handler(module_list: list, endswith: str = 'RequestHandler.py'):
    """
    自动将指定目录下以RequestHandler.py的文件加载，然后HandlerRouter的类变量中将保存加了装饰器的路由信息
    :param module_list:
    :param endswith:
    :return:
    """
    module_list = module_list or []
    _base_dir = os.path.join(os.path.dirname(__file__))
    _done_list = []
    for _ in module_list:
        _f_l = os.walk(_base_dir, _.replace('.', '/'))
        for _b, _folder_list, _file_list in _f_l:
            for _file in _file_list:
                if _file.endswith(endswith):
                    _package = _b[len(_base_dir) + 1:].replace('/', '.')
                    if f'{_package}.{_file[:-3]}' not in _done_list:
                        _app = importlib.import_module(name=f'.{_file[:-3]}', package=_package)
                        _done_list.append(f'{_package}.{_file[:-3]}')


class Config(object):
    def __init__(self):
        """
        系统配置对象
        配置对象的结构为：section.option.value
        :return:
        """
        self._conf_ = configparser.RawConfigParser()

    @staticmethod
    def _get_config_from_map_path_(path: str):
        """
        获取指定路径下的配置文件
        :param path:
        :return:
        """
        _conf = configparser.RawConfigParser()
        for _file_name in os.listdir(path):
            _file = os.path.join(path, _file_name)
            if os.path.isfile(_file):
                with open(_file, 'r') as _f:
                    _file_name_split = _file_name.split(".")
                    if len(_file_name_split) > 1:
                        _section = _file_name_split[0]
                        _conf_name = _file_name_split[1]
                        _conf_value = ''.join([x for x in _f.read().split("\n") if not x.startswith("#")])
                        if _section not in _conf.sections():
                            _conf.add_section(_section)
                        _conf.set(_section, _conf_name, _conf_value)
        return _conf

    def append_config(self, conf: str):
        """
        增加配置信息
        :param conf:
        :return:
        """
        _append = configparser.RawConfigParser()
        if conf.startswith("http://") or conf.startswith("https://"):
            res = request.urlopen(conf)
            _append.read_file(res)
        elif os.path.isdir(conf):
            _append = self._get_config_from_map_path_(conf)
        else:
            _append.read(conf, "utf-8")

        for sn in _append.sections():
            for attr in _append.options(sn):
                if sn not in self._conf_.sections():
                    self._conf_.add_section(sn)
                self._conf_.set(sn, attr, _append.get(sn, attr))

    def get_conf(self, _section, _key=None, conf_type=bytes, default=None):
        """
        读取配置
        :param _section:
        :param _key:
        :param conf_type:
        :param default:
        :return:
        """
        try:
            if _key is None:
                return self._conf_.items(_section)
            else:
                if bool == conf_type or conf_type == bool:
                    return self._conf_.getboolean(_section, _key)
                elif int == conf_type:
                    return int(self._conf_.get(_section, _key))
                else:
                    return self._conf_.get(_section, _key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set_conf(self, _section, _key, _value):
        """
        设置配置
        :param _section:
        :param _key:
        :param _value:
        :return:
        """
        if _section not in self._conf_.sections():
            self._conf_.add_section(_section)
        self._conf_.set(_section, _key, _value)

    def has_option(self, _section, _option):
        return _section in self._conf_.sections() and _option in self._conf_.options(_section)

    def get_options(self, section: str):
        """
        获取config所有section
        :return:
        """
        return self._conf_.options(section=section) if self._conf_.has_section(section=section) else None

    def get_sections(self):
        """
        获取一个配置对象下的所有section
        :return:
        """
        return self._conf_.sections()


class DataBaseUtil(object):
    """
    数据库连接对象
    """

    def __init__(self, db_path: str, read_path: str = None):
        """
        根据传入的数据库连接信息创建数据库连接
        读写区分，若未传入读连接则使用同一个engine对象
        :param db_path:
        :param read_path:
        """
        _engine = create_engine(
            db_path,
            pool_size=DB_POOL_SIZE,
            max_overflow=DB_MAX_OVERFLOW
        )
        _read_engine = create_engine(
            read_path,
            pool_size=DB_POOL_SIZE,
            max_overflow=DB_MAX_OVERFLOW
        ) if read_path else None
        self._db_engine = _engine
        self._db = sessionmaker(bind=_engine)()
        self._read = sessionmaker(bind=_read_engine)() if _read_engine else self._db

    @property
    def write(self):
        return self._db

    @property
    def read(self):
        return self._read

    @property
    def db(self):
        return self._db

    @property
    def db_engine(self):
        return self._db_engine


class UtilsObject(object):
    """
    工具初始化
    1、db
    2、file
    3、cache
    :return:
    """

    def __init__(self, config_path: str = None):
        """
        根据传入的config文件夹路径初始化基础组建信息
        :param config_path:
        """
        config_path = config_path or os.path.join(os.path.dirname(__file__), 'config')
        self._config = Config()
        os.path.isdir(config_path) and [
            self._config.append_config(os.path.join(config_path, _)) for _ in os.listdir(config_path)]
        self._db = self.init_db(self._config)
        self._redis = self.init_redis(self._config)
        self._document = self.init_document(self._config)

    @property
    def db(self):
        return self._db

    @property
    def redis(self):
        return self._redis

    @property
    def document(self):
        return self._document

    @property
    def config(self):
        return self._config

    def init_db(self, conf: object = None):
        """
        初始化db连接
        获取db连接参数，创建db连接对象
        :return:
        """
        _conf = conf or self._config
        _db_path = _conf.get_conf(_section='db', _key='db_path')
        _db_path_read = _conf.get_conf(_section='db', _key='db_path_read')
        return DataBaseUtil(db_path=_db_path, read_path=_db_path)

    def init_redis(self, conf: object = None):
        """
        初始化redis连接
        支持redis集群(默认单实例)
        :param conf:
        :return:
        """
        _conf = conf or self._config
        if _conf.get_conf(_section='redis', _key='redis_cluster'):
            _node_list = [
                {'host': _.split(':')[0], 'port': _.split(':')[1]}
                for _ in _conf.get_conf(_section='redis', _key='redis_cluster_nodes').split(',')
            ]
            return RedisCluster(
                startup_nodes=_node_list,
                decode_responses=True,
                password=_conf.get_conf(_section='redis', _key='redis_cluster_password'))
        else:
            return StrictRedis(
                connection_pool=ConnectionPool.from_url(_conf.get_conf(_section='redis', _key='redis_path')))

    def init_document(self, conf: object = None):
        """
        初始化文件路径
        :param conf:
        :return:
        """
        _conf = conf or self._config
        # 文件根目录
        _base_path = _conf.get_conf(
            _section='document',
            _key='base_path',
            default=None) or os.path.join(os.path.dirname(__file__), 'sources')
        # image目录
        _image_path = _conf.get_conf(_section='document', _key='image_path')
        _image_path = _image_path if _image_path.startswith('/') else os.path.join(_base_path, _image_path)
        # photo目录
        _photo_path = _conf.get_conf(_section='document', _key='photo_path')
        _photo_path = _photo_path if _photo_path.startswith('/') else os.path.join(_base_path, _photo_path)
        # document目录
        _document_path = _conf.get_conf(_section='document', _key='document_path')
        _document_path = _document_path if _document_path.startswith('/') else os.path.join(_base_path, _document_path)
        # workspace目录
        _workspace_path = _conf.get_conf(_section='document', _key='workspace_path')
        _workspace_path = _workspace_path if _workspace_path.startswith('/') else os.path.join(_base_path,
                                                                                               _workspace_path)
        return {
            'image': _image_path,
            'photo': _photo_path,
            'document': _document_path,
            'workspace': _workspace_path
        }


class HandlerRouter(object):
    _ruler_dict = {}

    def __init__(self, path: str):
        self._path = path

    def __call__(self, cls):
        HandlerRouter._ruler_dict.setdefault(self._path, cls)

    @classmethod
    def rule_dict(cls):
        return cls._ruler_dict


util_objet = UtilsObject()
