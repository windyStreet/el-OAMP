#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.logic.BO.OAMP.ExecFuncRecordBo import ExecFuncRecordBo
from bin import init
from bin.base.sys import SingleTableOpt
from bin.base.data import Data


class ExecFuncRecord(object):
    def __init__(self):
        pass

    # 查询消息列表
    def OAMP_search_exec_func_record_info_list(self, data):
        x = {
            '_id': data.get('_id'),
            'user_name__contains': data.get('user_name'),
            'msg__contains': data.get('msg'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ExecFuncRecordBo).search(filters=x, par=data)


    def record(self, data):
        SingleTableOpt.getInstance().setBO(ExecFuncRecordBo).setData(data).insert()


def getInstance():
    return ExecFuncRecord()
