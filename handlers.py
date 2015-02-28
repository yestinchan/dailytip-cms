# -*- coding:utf-8 -*-
__author__ = 'yestin'

from tornado import web
from config import config

import markdown2

from models import *
import utils

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
            user = self.get_current_user(),
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

class PagedIndexHandler(BaseHandler):
    def get(self,pageStr='0'):
        size = 7
        page = int(pageStr)
        # handle index.
        context = dict(config)
        posts = Post.list(self.db, page, size)
        tags = Tag.all(self.db)
        categories = Category.all(self.db)
        count = Post.count(self.db)
        totalPages = (count % size) and (count/size +1) or (count/size)
        context.update(dict(posts = posts, categories = categories, tags = tags, total_pages = totalPages, page =page))
        self.echo("index.html", context)

class ArchivesHanlder(BaseHandler):
    def get(self,pageStr='0'):
        size = 100
        page = int(pageStr)
        context = dict(config)
        posts = Post.list(self.db, page, size)
        # group by add time.
        groupedPosts = {}
        for post in posts:
            #convert html
            post.text = utils.HTMLUtils.no_tags(post.html)
            key =  post.add_time.strftime('%Y.%m')
            if key in groupedPosts.keys():
                groupedPosts[key].append(post)
            else:
                groupedPosts[key] = [post]
        print groupedPosts

        tags = Tag.all(self.db)
        categories = Category.all(self.db)
        count = Post.count(self.db)
        totalPages = (count % size) and (count/size +1) or (count/size)
        context.update(dict(grouped_posts = groupedPosts, categories = categories, tags = tags, total_pages = totalPages, page =page))
        self.echo("archives.html", context)

class PageHandler(BaseHandler):
    def get(self):
        # handle single page.
        self.write("page handler")

class PostHandler(BaseHandler):
    def get(self,idStr):
        id = int(idStr)
        post = Post.get(self.db,id)
        previous = Post.previous(self.db, id)
        next = Post.next(self.db, id)
        context = dict(config)
        context.update(dict(post = post, previous = previous, next = next))
        self.echo("post.html", context )


class AdminHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.write("Welcome admin!")


class AdminPostNewHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.echo('admin/posts/new.html')

class AdminPostEditHandler(BaseHandler):
    @web.authenticated
    def get(self):
        id = self.get_argument('id')
        post = Post.get(self.db,id)
        print post
        self.echo("admin/posts/edit.html",{'post':post})

class AdminPostListHandler(BaseHandler):
    @web.authenticated
    def get(self):
        size = 20
        page = int(self.get_argument('page',0))
        count = Post.count(self.db)
        totalPages = (count % size) and (count/size +1) or (count/size)
        print '{0},{1}'.format(page,size)
        posts = Post.list(self.db,page,size)
        self.echo('admin/posts/list.html',{'posts':posts,'total_pages': totalPages,'page':page})
        
class AdminPostAjaxSaveHandler(BaseHandler):
    @web.authenticated
    def post(self):
        title = self.get_argument('title')
        categories = self.get_argument('categories')
        tags = self.get_argument('tags')
        id = self.get_argument('id')
        content = self.get_argument('content')
        html = markdown2.markdown(content, extras=["footnotes","fenced-code-blocks"])
        if not id :
            result = Post.add(self.db, title,content,html,categories.split(','),tags.split(','))
        else:
            result = Post.update(self.db,id,title,content,html,categories.split(','),tags.split(','))
        return self.write('{{"id":{0}}}'.format(result))

class AdminPostAjaxPublishHandler(BaseHandler):

    @web.authenticated
    def post(self):
        title = self.get_argument('title')
        categories = self.get_argument('categories')
        tags = self.get_argument('tags')
        id = self.get_argument('id')
        content = self.get_argument('content')
        html = markdown2.markdown(content, extras=["footnotes","fenced-code-blocks"])
        if not id :
            result = Post.add(self.db, title,content,html,categories.split(','),tags.split(','),1)
        else:
            result = Post.update(self.db,id,title,content,html,categories.split(','),tags.split(','),1)
        return self.write('{{"id":{0}}}'.format(result))

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


