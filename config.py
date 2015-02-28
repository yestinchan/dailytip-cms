# -*- coding:utf-8 -*-
__author__ = 'yestin'

import os

settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__),"template"),
        xsrf_cookies=True,
        login_url="/admin/login",
        cookie_secret="s",
        autoescape=None,
        debug = True,
)

config = dict(
        db_host = "localhost",
        db_database = "dailytip",
        db_user = "yestin",
        db_pass = "yestinPass",
        db_idle_time = 10,
        site_title=u"Daily Tip",
        site_description=u"description",
        site_keywords=u"keywords",
)
