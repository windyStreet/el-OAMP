#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.ProjectTeamBo import ProjectTeamBo


class ProjectTeamManage(object):
    def __init__(self):
        pass

    # 查询项目信息
    def OAMP_search_project_team_info_list(self, data):
        x = {
            'id': data.get('_id'),
            'project_team__contains': data.get('project_team'),
            'project_team_name__contains': data.get('project_team_name'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ProjectTeamBo).search(filters=x, par=data)

    # 新增项目组信息
    def OAMP_insert_project_team_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectTeamBo).setData(data).insert()

    # 更新项目组信息
    def OAMP_update_project_team_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectTeamBo).setData(data).update()

    # 删除项目组信息
    def OAMP_delete_project_team_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectTeamBo).setData(data).delete()

    # 查询项目组code列表
    def OAMP_search_project_team_code_list(self, data):
        x = {}
        only = ['id', 'project_team_name']
        return SingleTableOpt.getInstance().setBO(ProjectTeamBo).search(filters=x, only=only)


def getInstance():
    return ProjectTeamManage()
