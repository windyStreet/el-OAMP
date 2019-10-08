#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.base.data import Path
from bin import init
from tornado import gen

htmlPath = Path.getInstance().webPath
context = init.CONF_INFO.get("server", {"context": ""}).get("context")


class html(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render(htmlPath + '/index.html')
