#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.logic.func.setting.projectManage import Project
from bin.logic.func.setting import ServerSetting
from bin.logic.func.setting import ServiceContainerConf
from bin.logic.func.common import Link
from bin.logic.func.task import ServiceCheckTask
from bin.logic.func.setting.projectManage import ProjectUpdateConf
from bin.logic.func.setting.projectManage import ProjectOptRecord


class MQ_logic(object):
    def __init__(self):
        pass

    # 静态文件更新
    def MQ_project_static_file_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).MQ_project_static_file_update(data)

    # 全量更新
    def MQ_project_full_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).MQ_project_full_update(data)

    # 增量更新
    def MQ_project_increase_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).MQ_project_increase_update(data)

    # 项目重启
    def MQ_project_restart(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).MQ_project_restart(data)


def getInstance():
    return MQ_logic()
