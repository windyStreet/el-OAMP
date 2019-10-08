#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from tornado import gen
from tornado import process
from bin.base.sys.Session import SessionHandler
from bin.logic.Service_logic import *
from bin.logic import Service_logic as Menu
from bin.base.sys import PR
import json
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor


class Service(SessionHandler, tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(process.cpu_count())

    # @tornado.web.asynchronous #gen.coroutine 在 Tornado 3.1 后会自动调用 self.finish() 结束请求，可以不使用 asynchronous 装饰器
    @gen.coroutine
    def post(self):
        result = yield self.done()
        self.write(result)

    @run_on_executor
    def done(self, *args, **kwargs):
        __sessionId__ = self.session_obj.random_str
        method = 'default_method'
        _PR = PR.getInstance()
        try:
            request_body = str(self.request.body, encoding="utf-8")
            if request_body is None or request_body == "":
                _PR.setCode(PR.Code_PARERROR)
                _PR.setMsg("not set the request data")
                return _PR.json()
            req = json.loads(request_body)
            method = req.get('serviceName', '__error__')
            if method == "__error__":
                _PR.setCode(PR.Code_METHODERROR)
                _PR.setMsg("method ERROR , not give the method or get the method is __error__")
                return _PR.json()
            data = req.get('data', None)
            data['__sessionId__'] = __sessionId__
            # 在此处处理session问题[每次去查询session信息，太多，如何处理?]
            L.debug("%s service par is %s" % (method, data))
            menu = Menu.getInstance()
            return getattr(menu, method)(data).json()
        except Exception as e:
            _PR.setCode(PR.Code_EXCEPTION).setMsg(" %s service exception : %s" % (method, str(e)))
            L.exception(" %s service exception : %s" % (method, str(e)))
            return _PR.json()

    @gen.coroutine
    def get(self):
        self.post()


##uploadFile
class uploadFile(SessionHandler, tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(process.cpu_count())

    @gen.coroutine
    def post(self):
        result = yield self.done()
        self.write(result)

    @run_on_executor
    def done(self, *args, **kwargs):
        __sessionId__ = self.session_obj.random_str
        _PR = PR.getInstance()
        method = 'default_method'
        try:
            arguments = self.request.body_arguments
            par = {}
            for (k, v) in arguments.items():
                par[k] = str(v[0], encoding="utf8")
            par['content'] = self.request.files['true'][0].get('body')
            method = par.get('serviceName', '__error__')
            if method == "__error__":
                _PR.setCode(PR.Code_METHODERROR)
                _PR.setMsg("method ERROR , not give the method or get the method is __error__")
                return _PR.json()
            par['__sessionId__'] = __sessionId__
            # 在此处处理session问题[每次去查询session信息，太多，如何处理?]
            # L.debug("%s service par is %s" % (method, par))
            L.debug("%s service " % method)
            menu = Menu.getInstance()
            return getattr(menu, method)(par).json()
        except Exception as e:
            _PR.setCode(PR.Code_EXCEPTION).setMsg(" %s service exception : %s" % (method, str(e)))
            L.exception(" %s service exception : %s" % (method, str(e)))
            return _PR.json()


class Open_falcon_query(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(process.cpu_count())

    @gen.coroutine
    def post(self):
        result = yield self.done()
        self.write(result)

    @run_on_executor
    def done(self, *args, **kwargs):
        _PR = PR.getInstance()
        try:
            if self.request.arguments is None or self.request.arguments == "":
                _PR.setCode(PR.Code_PARERROR)
                _PR.setMsg("not set the request data")
                return self._PR.json()
            content = self.get_arguments("content")
            subject = self.get_arguments("subject")
            tos = str(self.get_argument("tos")).replace('[', '').replace(']', '').split(',')
            data = {
                "content": content,
                "subject": subject,
                "tos": tos
            }
            menu = Menu.getInstance()
            return getattr(menu, 'mail_falcon')(data).json()
        except Exception as e:
            _PR.setCode(PR.Code_EXCEPTION).setMsg(" %s service exception : %s" % ('Open_falcon_query', str(e)))
            L.exception(" %s service exception : %s" % ('Open_falcon_query', str(e)))
            return _PR.json()



