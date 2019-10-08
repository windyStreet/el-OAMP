#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import redis
import json
from bin import init

class Redis(object):
    def __init__(self, ds, host, port, db, password):
        if ds is not None:
            redis_conf_info = init.CONF_INFO[ds]
            host = redis_conf_info.get('toolHost')
            port = redis_conf_info.get('toolPort')
            password = redis_conf_info.get('toolPassword')

        # self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        pool = redis.ConnectionPool(max_connections=100, host=host, port=port, db=db, password=password)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def setJson(self, key, value, ex):
        data = {}
        if value is None:
            return None
        for k in value.keys():
            val = value.get(k)
            if val is None:
                continue
            if val is True:
                val = 1
            data[k] = val
        return self.redis.set(name=key, value=json.dumps(data, ensure_ascii=False), ex=ex)

    def delJson(self, key):
        return self.redis.delete(key)

    def getJson(self, key):
        redis_data = self.redis.get(key)
        if redis_data is None:
            return None
        return json.loads(str(redis_data, encoding="utf-8"))

    # 对key添加锁
    def add_lock(self, key, ttl):
        if self.getJson(key=key) is not None:
            return False  # 目标锁已经存在
        self.setJson(key=key, value={'file_lock': '1'}, ex=ttl)
        return True

    # 释放对象锁
    def release_lock(self, key):
        return self.delJson(key=key)


def getInstance(ds=None, host='127.0.0.1', port=6379, db=0, password=None):
    return Redis(ds=ds, host=host, port=port, db=db, password=password)
