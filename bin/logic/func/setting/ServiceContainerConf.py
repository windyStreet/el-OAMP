#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.data import Data
from bin.logic import Inner_logic
from bin.base.sys import PR
from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.ServiceContainerBo import ServiceContainerBo


class ServiceContainerConf(object):
    def __init__(self):
        pass

    # 查询服务容器信息列表
    def OAMP_search_service_container_list(self, data):
        x = {
            'belong_to_server_id': data.get('belong_to_server_id', None),
            'service_container_name__contains': data.get('service_container_name'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ServiceContainerBo).search(filters=x, par=data)

    # 新增服务容器信息
    def OAMP_insert_service_container_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServiceContainerBo).setData(data).insert()

    # 更新服务容器信息
    def OAMP_update_service_container_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServiceContainerBo).setData(data).update()

    # 删除服务容器信息
    def OAMP_delete_service_container_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServiceContainerBo).setData(data).delete()

    # 通过项目id和服务器id获取该服务器上项目服务容器信息
    # 1、查询 服务器中的 服务容器信息 【容器id、 所属服务id】
    # 2、查询 项目-容器列表 ， 获取 容器id
    # 3、取容器id交集部分
    # 4、过滤出容器信息部分，组装返回
    def OAMP_search_service_container_info_list_by_project_id_and_server_id(self, data):
        server_id = data.get('server_id')
        project_id = data.get('project_id')
        if server_id is None or project_id is None:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('通过项目id和服务器id，查询当前服务器中项目关联的服务容器信息,参数错误')
        else:
            _service_container_res = self.OAMP_search_service_container_list({'belong_to_server_id': server_id})
            _linked_res = Inner_logic.getInstance().search_link_info_by_link_id(link_id=project_id, link_type_code_id='2')
            if _service_container_res.is_results_not_none() and _linked_res.is_results_not_none():
                server_container_id = []
                linked_id = []
                for _service_container_re in _service_container_res.getData():
                    server_container_id.append(_service_container_re.get('_id'))
                for link in _linked_res.getData():
                    linked_id.append(link.get('linked_id'))
                intersection_list = list(set(server_container_id).intersection(set(linked_id)))
                result = []
                for _service_container_re in _service_container_res.getData():
                    if _service_container_re.get('_id') in intersection_list:
                        result.append(_service_container_re)
                return PR.getInstance().setCode(PR.Code_OK).setResult({'data': result}).setMsg('通过项目id和服务器id获取该服务器上项目服务容器信息')
            else:
                return PR.getInstance().setCode(PR.Code_OK).setResult({'data': []}).setMsg('通过项目id和服务器id获取该服务器上项目服务容器信息，未查询到服务容器信息或者项目关联服务容器信息')


def getInstance():
    return ServiceContainerConf()
