#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import SingleTableOpt, PR
from bin.logic.BO.OAMP.ProjectBo import ProjectBo
from bin.logic import Inner_logic


class Project(object):
    def __init__(self):
        pass

    # 查询项目信息
    def OAMP_search_project_list(self, data):
        x = {
            'id': data.get('_id'),
            'project_state_code_id': data.get('project_state_code_id', None),
            'project_type_code_id': data.get('project_type_code_id'),
            'project__contains': data.get('project'),
            'project_name__contains': data.get('project_name'),
            'project_context__contains': data.get('project_context'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ProjectBo).search(filters=x, par=data)

    # 新增项目信息
    def OAMP_insert_project_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectBo).setData(data).insert()

    # 更新项目信息
    def OAMP_update_project_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectBo).setData(data).update()

    # 删除项目信息
    def OAMP_delete_project_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectBo).setData(data).delete()

    # 获取项目code列表信息
    def OAMP_search_project_code_list(self, data):
        x = {
            'id': data.get('_id', ),
            'project_type_code_id': data.get('project_type_code_id'),
            'project': data.get('project'),
            'project_team_id': data.get('project_team_id'),
        }
        only = ['id', 'project', 'project_name']
        return SingleTableOpt.getInstance().setBO(ProjectBo).search(filters=x, only=only)

    # 通过id查询项目信息
    def OAMP_search_project_info_by_id(self, data):
        par = {'_id': data.get('project_id')}
        return SingleTableOpt.getInstance().setBO(ProjectBo).setData(data=par).search()

    # 查询项目关联服务器列表
    def OAMP_search_project_server_list(self, data):
        # 1、查询服务器列表
        project_id = data.get('project_id', None)
        if project_id is None:
            return PR.getInstance().setCode(PR.Code_PARERROR).setResult({}).setMsg('par error , miss [project_id]')
        _server_res = Inner_logic.getInstance().search_server_list(par=data)
        if _server_res.is_results_not_none():
            # 2、查询关联信息
            _link_res = Inner_logic.getInstance().search_link_info_by_link_id(link_id=project_id, link_type_code_id='1')
            res = []
            # 3、数据处理
            for server_data in _server_res.getData():
                server_data['is_project_server_link'] = '0'
                if _link_res.is_results_not_none():
                    for link_data in _link_res.getData():
                        if server_data.get('_id') == link_data.get('linked_id'):
                            server_data['is_project_server_link'] = '1'
                            server_data['link_info_id'] = link_data.get('_id')
                            break
                res.append(server_data)
            _server_res.setData(res)
        return _server_res

    # 查询项目关联服务容器列表
    def OAMP_search_project_server_container_list(self, data):
        # 1、查询服务容器列表
        project_id = data.get('project_id', None)  # 项目id
        if project_id is None:
            return PR.getInstance().setCode(PR.Code_PARERROR).setResult({}).setMsg('par error , miss [project_id]')
        _service_container_res = Inner_logic.getInstance().search_service_container_list(par=data)  # 该服务器拥有的容器
        if _service_container_res.is_results_not_none():
            res = []
            for service_data in _service_container_res.getData():
                _linked_res = Inner_logic.getInstance().search_link_info_by_linked_id(linked_id=service_data.get('_id'), link_type_code_id='2')  # 服务器已被使用的容器
                if _linked_res.is_results_not_none():  # 当前容器是否已经被使用
                    _linked_data = _linked_res.getData()
                    service_data['link_info_id'] = _linked_data[0].get('_id')
                    if _linked_data[0].get('link_id') == project_id:  # 看看是不是被当前项目使用
                        service_data['is_service_container_link'] = '1'  # 当前服务容器被当前项目使用
                    else:  # 当前服务容器被其他项目使用
                        service_data['is_service_container_link'] = '2'
                else:  # 当前容器未被使用
                    service_data['is_service_container_link'] = '0'  # 该服务器的容器状态先置为未被使用状态
                res.append(service_data)
            _service_container_res.setData(res)
        return _service_container_res


def getInstance():
    return Project()
