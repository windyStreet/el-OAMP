#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from bin.base.tool import Redis
from bin.base.log import Logger
from hashlib import sha1
from bin import init

L = Logger.getInstance()
# 生成一个随机的session_id
create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()
session_id = "__sessionId__"

# 出现调用链问题，导致init类未加载 to fixed

R = Redis.getInstance(ds=init.ROOT_REDIS_DS, db=init.DEFAULT_SESSION_REDIS_DB)


class SessionHandler:
    def initialize(self):
        self.session_obj = SessionData(self)



        # self.session_obj = SessionFactory.get_session_obj(self)


class SessionData(object):
    def __init__(self, handler):

        self.handler = handler
        self.sessionInfo = {}
        client_random_str = handler.get_cookie(session_id, None)  # 查看前端的session_id 是否消失[消失，怎用户登录已经失效，应该默认转跳至登录页]
        if client_random_str is not None:
            self.random_str = client_random_str
            self.sessionInfo = SessionDataOpt(self.random_str).getSession()
        else:
            self.random_str = create_session_id()
        expires_time = time.time() + init.DEFAULT_SESSION_EXPIRE_TIME
        handler.set_cookie(session_id, self.random_str, expires=expires_time)
        R.setJson(key=self.random_str, value=self.sessionInfo, ex=init.DEFAULT_SESSION_EXPIRE_TIME)

    def getSessionObj(self, handler):
        return SessionData(handler)


class SessionDataOpt(object):
    def __init__(self, sessionId):
        self.sessionId = sessionId

    def getUserName(self):
        return R.getJson(self.sessionId).get('userName', 'sys')

    def getSession(self):
        return R.getJson(self.sessionId)

    def setSession(self, value, ex):
        return R.setJson(key=self.sessionId, value=value, ex=ex)

    def delSession(self):
        return R.delJson(key=self.sessionId)

    def getSessionData(self, key):
        data = self.getSession()
        if data is None:
            return None
        res = data.get(key)
        return res
