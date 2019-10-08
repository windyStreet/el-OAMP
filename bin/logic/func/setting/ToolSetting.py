#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin import init
from bin.base.sys import SingleTableOpt, PR
from bin.base.sys.Bean import Bean
from mongoengine import Q
from bin.base.db.MongoEng import MongoEng
from bin.logic.BO.OAMP.ToolBo import ToolBo


class ToolSetting(object):
    def __init__(self):
        pass

    # 查询工具列表信息
    def OAMP_search_tool_list(self, data):
        x = {
            'tool_type_code_id': data.get('tool_type_code_id', None),
            'toolName__contains': data.get('toolName', None),
            'toolPort': data.get('toolPort', None),
            'toolHost': data.get('toolHost', None),
            'toolUser__contains': data.get('toolUser')
        }
        return SingleTableOpt.getInstance().setBO(ToolBo).search(filters=x, par=data)

    # 删除工具信息
    def OAMP_delete_tool_info(self, data):
        return SingleTableOpt.getInstance().setBO(ToolBo).setData(data).delete()

    # 新增工具信息
    def OAMP_insert_tool_info(self, data):
        return SingleTableOpt.getInstance().setBO(ToolBo).setData(data).insert()

    # 修改工具信息
    def OAMP_update_tool_info(self, data):
        return SingleTableOpt.getInstance().setBO(ToolBo).setData(data).update()

    # 获取工具信息
    def OAMP_get_tool_info(self, data):
        x = {
            'tool_project_id': data.get('tool_type_code_id')
        }
        return SingleTableOpt.getInstance().setBO(ToolBo).search(filters=x)

    # # 查询CDN项目类型信息
    # def OAMP_getToolInfoByType(self, data):
    #     _PR = PR.getInstance()
    #     x = {
    #         'toolCodeId': data.get('toolCodeId')
    #     }
    #     f = Q(**Bean().getSearchBean(x))
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     res = ToolBo.objects.filter(f).only('toolRootPath', 'toolProject', 'toolProjectName')
    #     return _PR.setResult(res).setCode(PR.Code_OK).setMsg("查询工具类型信息成功")


def getInstance():
    return ToolSetting()
