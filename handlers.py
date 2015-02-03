# -*- coding:utf-8 -*-
__author__ = 'yestin'

from tornado import web
from config import config

from models import *

class BaseHandler(web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_name = self.get_secure_cookie("user")
        return user_name

    def render(self, file, context=None):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )

        context.update(args)
        template = self.application.template_env.get_template(file)
        return template.render(context)

    def echo(self, template, context = None):
        self.write(self.render(template,context))

class IndexHandler(BaseHandler):
    def get(self):
        # handle index.
        context = dict(config)
        self.echo("index.html", context)

class PageHandler(BaseHandler):
    def get(self):
        # handle single page.
        self.write("page handler")

class PostHandler(BaseHandler):
    def get(self,args):
        self.write("post handler")


class AdminHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.write("Welcome admin!")

class AdminLoginHandler(BaseHandler):
    def get(self, error = None):
        self.echo("admin/login.html",  {"error":error})

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        user = User.get(self.db, name, password )
        if user is None:
            self.redirect("/admin/login?error=True")
        self.set_secure_cookie("user", str(user.name))
        print "set done"
        self.redirect(self.get_argument("next", "/admin/"))


