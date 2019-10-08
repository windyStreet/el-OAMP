#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.sys import SingleTableOpt, PR
from bin.logic.BO.OAMP.LinkBo import LinkBo


class Link(object):
    def __init__(self):
        pass

    # 新增关联信息
    def OAMP_insert_link_info(self, data):
        return SingleTableOpt.getInstance().setBO(LinkBo).setData(data=data).insert()

    # 删除关联信息
    def OAMP_delete_link_info(self, data):
        return SingleTableOpt.getInstance().setBO(LinkBo).setData(data=data).delete()

    def OAMP_search_link_info_by_link_id(self, data):
        link_id = data.get('link_id', None)
        link_type_code_id = data.get('link_type_code_id', None)
        if link_id is None or link_type_code_id is None:
            return PR.getInstance().setCode(PR.Code_PARERROR).setResult({}).setMsg('par error [link_id ,link_type_code_id]')
        x = {
            'link_id': link_id,
            'link_type_code_id': link_type_code_id
        }
        return SingleTableOpt.getInstance().setBO(LinkBo).search(filters=x)

    #  查询 linked_id [内部调用方法]
    def _search_link_info_by_link_id(self, link_id, link_type_code_id):
        link_x = {
            'link_id': link_id,
            'link_type_code_id': link_type_code_id
        }
        return SingleTableOpt.getInstance().setBO(LinkBo).search(filters=link_x, only=['id','linked_id'])

    #  查询 linked_id [内部调用方法]
    def _search_link_info_by_linked_id(self, linked_id, link_type_code_id):
        link_x = {
            'linked_id': linked_id,
            'link_type_code_id': link_type_code_id
        }
        return SingleTableOpt.getInstance().setBO(LinkBo).search(filters=link_x, only=['id','link_id'])



def getInstance():
    return Link()
