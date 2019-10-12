#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.logic.func.setting.projectManage import Project
from bin.logic.func.setting import ServerSetting
from bin.logic.func.setting import ServiceContainerConf
from bin.logic.func.common import Link
from bin.logic.func.task import ServiceCheckTask
from bin.logic.func.setting.projectManage import ProjectUpdateConf
from bin.logic.func.setting.projectManage import ProjectOptRecord
from bin.logic.func.setting.sysManage import RoleManage
from bin.logic.func.setting.sysManage import SysRouterManage


class Inner_logic(object):
    def __init__(self):
        pass

    # 通过link_id 查询关联信息 {_id,linked_id}
    def search_link_info_by_link_id(self, link_id, link_type_code_id):
        return Link.getInstance()._search_link_info_by_link_id(link_id, link_type_code_id)

    # 通过linked_id 查询关联信息{_id,link_id}
    def search_link_info_by_linked_id(self, linked_id, link_type_code_id):
        return Link.getInstance()._search_link_info_by_linked_id(linked_id, link_type_code_id)

    # 查询服务器列表
    def search_server_list(self, par):
        return ServerSetting.getInstance().OAMP_search_server_list(par)

    # 获取项目服务检查信息
    def get_project_service_check_info(self, service_project_id):
        return ServiceCheckTask.getInstance().get_project_service_check_info(service_project_id)

    # 更新项目信息
    def update_project_info(self, data):
        return Project.getInstance().OAMP_update_project_info(data=data)

    # 通过项目id 查询项目更新配置信息
    def search_project_update_conf_info_by_project_id(self, data):
        return ProjectUpdateConf.getInstance().OAMP_search_project_update_conf_info_list(data=data)

    # 查询项目信息通过 {'project_id':''}
    def search_project_info_by_id(self, data):
        return Project.getInstance().OAMP_search_project_info_by_id(data=data)

    # server相关
    # 通过项目id查询项目所在的服务器信息
    def search_server_list_by_project_id(self, data):
        return ServerSetting.getInstance().OAMP_search_server_list_by_project_id(data=data)

    # 查询服务容器列表
    def search_service_container_list(self, par):
        return ServiceContainerConf.getInstance().OAMP_search_service_container_list(par)

    # 通过项目id和服务器id获取该服务器上项目服务容器信息
    def search_service_container_info_list_by_project_id_and_server_id(self, data):
        return ServiceContainerConf.getInstance().OAMP_search_service_container_info_list_by_project_id_and_server_id(data=data)

    # 通过id查询项目操作记录信息
    def search_project_opt_record_info_by_id(self, data):
        _id = data.get('_id')
        return ProjectOptRecord.getInstance().OAMP_search_project_opt_record_info_by_id(data={'_id': _id})

    # 更新项目曹组记录信息
    def update_project_opt_record_info(self, data):
        return ProjectOptRecord.getInstance().OAMP_update_project_opt_record_info(data=data)

    # 查询角色代码列表
    def search_role_code_list(self, data):
        return RoleManage.getInstance().OAMP_search_role_code_list(data)

    # 查询系统路由信息列表
    def search_sys_router_info_list(self, data, only):
        return SysRouterManage.getInstance().OAMP_search_sys_router_info_list(data, only)


def getInstance():
    return Inner_logic()
