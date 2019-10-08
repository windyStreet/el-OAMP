#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.logic.BO.OAMP.MsgBo import MsgBo
from bin import init
from bin.base.sys import SingleTableOpt
from bin.base.data import Data


class MsgRecord(object):
    def __init__(self):
        pass

    # 查询消息列表
    def OAMP_search_msg_info_list(self, data):
        x = {
            'user_name__contains': data.get('user_name'),
            'msg__contains': data.get('msg'),
            'msg_type_code_id': data.get('msg_type_code_id'),
            'msg_level_code_id': data.get('msg_level_code_id'),
            'send_time__gte': data.get('send_time')[0] if data.get('send_time') is not None and len(data.get('send_time')) >= 1 else '',
            'send_time__lt': data.get('send_time')[1] if data.get('send_time') is not None and len(data.get('send_time')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(MsgBo).search(filters=x, par=data)


    def record(self, data):
        par = data.get('par')
        data['par'] = Data.json_to_str(par)
        SingleTableOpt.getInstance().setBO(MsgBo).setData(data).insert()


def getInstance():
    return MsgRecord()
