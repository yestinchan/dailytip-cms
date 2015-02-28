#-*- coding:utf-8 -*-
__author__ = 'Yestin'

import re

class HTMLUtils:
    @classmethod
    def no_tags(cls,html):
        re_html=re.compile('</?\w+[^>]*>')#HTML标签
        result = re_html.sub('',html)
        return result
