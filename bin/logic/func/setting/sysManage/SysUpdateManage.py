#!/usr/bin/env python
# !-*- coding: utf-8-*-
from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.SysUpdateBo import SysUpdateBo


class SysUpdateMange(object):
    def __init__(self):
        pass

    # 新增系统更新信息
    def OAMP_insert_sys_update_info(self, data):
        return SingleTableOpt.getInstance().setBO(SysUpdateBo).setData(data).insert()

    # 修改系统更新信息
    def OAMP_update_sys_update_info(self, data):
        return SingleTableOpt.getInstance().setBO(SysUpdateBo).setData(data).update()

    # 删除更新信息插入
    def OAMP_delete_sys_update_info(self, data):
        return SingleTableOpt.getInstance().setBO(SysUpdateBo).setData(data).delete()

    # 查询系统更新信息列表
    def OAMP_search_sys_update_info_list(self, data):
        x = {
            'version_number__contains': data.get('version_number'),
            'version_content__contains': data.get('version_content'),
            'version_update_time__gte': data.get('version_update_time')[0] if data.get('version_update_time') is not None and len(
                data.get('version_update_time')) >= 1 else '',
            'version_update_time__lt': data.get('version_update_time')[1] if data.get('version_update_time') is not None and len(
                data.get('version_update_time')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(SysUpdateBo).search(filters=x, par=data)


def getInstance():
    return SysUpdateMange()
