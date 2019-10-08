#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.tool import JsonFileFunc
from bin.base.data import Path
from bin.base.log import Logger
from bin.logic.BO.OAMP.ToolBo import ToolBo
from bin.base.db.MongoEng import MongoEng
from bin.base.sys.Bean import Bean
from mongoengine import Q
import json

J = JsonFileFunc.getInstance()
P = Path.getInstance()
L = Logger.getInstance('sys.log')


class ConfInit(object):
    def __init__(self):
        pass

    # 数据库配置文件初始化
    def DBConfInit(self):
        context = init.CONTEXT
        # 查询数据库 按照文件格式进行分配
        x = {
            'toolContext': context
        }
        f = Q(**Bean().getSearchBean(x))
        MongoEng(init.ROOT_DB_DS).getCollection()
        res = ToolBo.objects.filter(f)
        for item in res:
            data = json.loads(item.to_json())
            key = data.get('tool_type_code_id')
            init.CONF_INFO[context + key] = data
        L.debug('初始化参数[init.CONF_INFO]值为: %s' % init.CONF_INFO)

    def init(self):
        # 系统默认配置文件在类加载时已经执行
        self.DBConfInit()  # 数据库配置文件初始化
        pass


def getInstance():
    return ConfInit()
