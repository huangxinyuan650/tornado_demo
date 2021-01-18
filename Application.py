# _*_ coding:utf-8_*_
# Author:   Ace Huang
# Time: 2021/1/15 09:37
# File: Application.py

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado import httpserver
from tornado.options import options, define
import logging
import os
from utils import util_objet, import_handler
from utils import HandlerRouter

logging.basicConfig(level=logging.INFO)

define(name='port', default=2650, type=int, help='Default Server Port')
options.parse_command_line()




def main():
    """
    1、引入SqlAlchemy
    2、引入Redis
    3、增加读写分离
    4、增加分区分表
    5、自动加载指定目录下的指定RequestHandler
    :return:
    """
    import_handler(module_list=[_a for _, _a in util_objet.config.get_conf(_section='app')])
    _handlers = [(_r, _h, dict(utils=util_objet)) for _r, _h in HandlerRouter.rule_dict().items()]
    _application = Application(
        handlers=_handlers,
        template_path=os.path.join(os.path.dirname(__file__), 'template'))
    _http_server = httpserver.HTTPServer(_application, xheaders=True)
    _http_server.listen(util_objet.config.get_conf(_section='base', _key='port') or options.port)
    logging.info(f'Server is listening port:{options.port}')
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
