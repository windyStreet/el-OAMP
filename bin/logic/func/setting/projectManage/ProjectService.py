#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import PR
from bin.logic import Inner_logic
from bin.base.log import Logger
from bin.base.data import Data


L = Logger.getInstance()


# 项目服务类
class ProjectService(object):
    def __init__(self):
        pass

    # 检查项目服务状态
    def check_project_service_status(self):
        pass

    # 判断项目服务状态
    # 查询到serviceBO对象的状态
    # 全部正常，正常的
    # 有一个挂了，异常
    # 都挂了，停止
    # 有检查服务停止的怎么处理
    # MQ
    def judge_project_service_status(self, service_project_id):
        service_check_res = Inner_logic.getInstance().get_project_service_check_info(service_project_id=service_project_id)
        count = 0
        normal_count = 0
        pause_count = 0
        error_count = 0
        if service_check_res.is_results_not_none():
            for service_check_info in service_check_res.getData():
                count += 1
                if service_check_info.get('service_state_code_id', '1') == '1' and service_check_info.get('service_check_state_code_id') == '1':
                    normal_count += 1
                elif service_check_info.get('service_check_state_code_id') == '2':  # 暂停
                    pause_count += 1
                    pass
                else:  # 有问题
                    error_count += 1
        if normal_count is count - pause_count:  # 暂停项目不用理会
            project_service_state_code_id = '1'  # 项目服务状态 正常
        elif 0 < error_count < count - pause_count:
            project_service_state_code_id = '-1'  # 项目服务状态 异常
        elif error_count is count - pause_count:
            project_service_state_code_id = '0'  # 项目服务状态 不可用
        else:
            project_service_state_code_id = '2'  # 项目服务状态 未知
        project_container_status = ('【%s】【%s】【%s】【%s】' % (str(error_count), str(pause_count), str(normal_count), str(count)))
        p_re = Inner_logic.getInstance().search_project_info_by_id({'project_id': service_project_id})
        if p_re.is_result_not_none():
            item = p_re.getData()
            item['project_service_state_code_id'] = project_service_state_code_id
            item['project_container_status'] = project_container_status
            return Inner_logic.getInstance().update_project_info(data=item)
        else:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('不存在该项目信息')

    def MQ_start(self, msg_data):
        par = msg_data.get('par')
        if par is not None:
            service_project_id = Data.str_to_json(par).get('service_project_id')
            self.judge_project_service_status(service_project_id=service_project_id)
        else:
            L.exception('MQ_start for judge_project_service_status not get the right par ')


def getInstance():
    return ProjectService()
