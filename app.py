#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'yestin'

from tornado import ioloop,web
import tornado
import os

import torndb

from jinja2 import Environment, FileSystemLoader

from config import settings, config
import handlers


class Application(tornado.web.Application):
    def __init__(self,route,settings):
        web.Application.__init__(self, route, **settings)
        # i18n
        #tornado.locale.load_gettext_translations(self.settings['i18n_path'], "dailtip")
        self.db = torndb.Connection(
                host=config['db_host'], database=config['db_database'],
                user=config['db_user'], password=config['db_pass'], max_idle_time=config['db_idle_time'])

        self.template_env = Environment(loader=FileSystemLoader(settings['template_path']))



route = list([
    (r"/",handlers.IndexHandler ),
    (r"/post/(.*)",handlers.PostHandler),
    (r"/admin/login", handlers.AdminLoginHandler),
    (r"/admin/",handlers.AdminHandler),
    (r"/(.*)",handlers.PageHandler),
])


def main():
    app = Application(route,settings)
    app.listen(8888)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("exit")
        ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    main()