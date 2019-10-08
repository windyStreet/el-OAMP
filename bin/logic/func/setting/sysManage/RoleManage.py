#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.RoleBo import RoleBo


class RoleManage(object):
    def __init__(self):
        pass

    # 查询角色信息
    def OAMP_search_role_info_list(self, data):
        x = {
            'id': data.get('_id'),
            'role_name__contains': data.get('role_name'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(RoleBo).search(filters=x, par=data)

    # 新增角色信息
    def OAMP_insert_role_info(self, data):
        return SingleTableOpt.getInstance().setBO(RoleBo).setData(data).insert()

    # 更新角色信息
    def OAMP_update_role_info(self, data):
        return SingleTableOpt.getInstance().setBO(RoleBo).setData(data).update()

    # 删除角色信息
    def OAMP_delete_role_info(self, data):
        return SingleTableOpt.getInstance().setBO(RoleBo).setData(data).delete()


    # 查询角色代码列表信息
    def OAMP_search_role_code_list(self, data):
        x = {
            'role_type_code_id': data.get('role_type_code_id'),
        }
        only = ['id', 'role_name']
        return SingleTableOpt.getInstance().setBO(RoleBo).search(filters=x, only=only)


def getInstance():
    return RoleManage()
