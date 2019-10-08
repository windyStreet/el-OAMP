#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import connect
from bin import init


class MongoEng(object):
    def __init__(self, ds=None):
        _db_info = init.CONF_INFO.get(ds)
        self.ip = _db_info.get('toolHost')
        self.port = _db_info.get('toolPort')
        self.db = _db_info.get('toolName')
        self.user = _db_info.get('toolUser')
        self.password = _db_info.get('toolPassword')
        self.collection = None
        pass

    def getCollection(self):
        self.collection = connect(db=self.db, host=self.ip, port=self.port, username=self.user, password=self.password)
        return self.collection
