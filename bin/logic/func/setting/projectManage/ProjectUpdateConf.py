#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.log import Logger
from bin.logic.BO.OAMP.ProjectUpdateConfBo import ProjectUpdateConfBo
from bin.base.sys import PR
from bin.base.sys import SingleTableOpt
from bin.logic import Inner_logic
from bin.base.sys import Msg
from bin.base.tool import RabbitMQ
from bin import init
from bin.base.data import PostUntil
import os
import copy

L = Logger.getInstance()


# 项目服务类
class ProjectUpdateConf(object):
    def __init__(self):
        pass

    # 查询项目更新配置信息列表
    def OAMP_search_project_update_conf_info_list(self, data):
        x = {
            'id': data.get('_id'),
            'project_team_id': data.get('project_team_id', None),
            'project_id': data.get('project_id', None),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ProjectUpdateConfBo).search(filters=x, par=data)

    # 插入项目更新配置信息
    def OAMP_insert_project_update_conf_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectUpdateConfBo).setData(data).insert()

    # 修改项目更新配置信息
    def OAMP_update_project_update_conf_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectUpdateConfBo).setData(data).update()

    # 删除项目更新配置信息
    def OAMP_delete_project_update_conf_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectUpdateConfBo).setData(data).delete()

    # 1、获取项目新
    # 2、获取项目服务器相关信息
    # return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('远程重建更新配置文件成功')
    # 重建远程配置文件
    def OAMP_rebuild_remote_update_conf(self, data):
        __sessionId__ = data.get('__sessionId__')
        project_id = data.get('project_id')
        if project_id is None:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': '0'}).setMsg('远程重建更新配置文件,参数错误')
        agent_service_url = data.get('agent_service_url')
        update_share_bak_path = data.get('update_share_bak_path')
        update_share_conf_bak_path = data.get('update_share_conf_bak_path')
        upstream_conf_file = data.get('upstream_conf_file')
        redis_ip = data.get('redis_ip')
        redis_port = data.get('redis_port')
        redis_password = data.get('redis_password')
        _re = Inner_logic.getInstance().search_project_info_by_id({'project_id': project_id})  # 查询项目信息
        _re_data = _re.getData()
        project_check_service = _re_data.get('project_check_service')
        project_context = _re_data.get('project_context')
        project = _re_data.get('project')
        project_name = _re_data.get('project_name')
        project_type_code_id = _re_data.get('project_type_code_id')
        project_default_root_path = _re_data.get('project_default_root_path')
        if _re.is_result_not_none():
            _res1 = Inner_logic.getInstance().search_server_list_by_project_id({'project_id': project_id})  # 通过项目项目信息查询服务器信息
            if _res1.is_results_not_none():
                po_ins = PostUntil.getInstance()
                for re in _res1.getData():
                    # 循环调用远程接口，生成配置文件
                    server_id = re.get('_id')  # 服务器id
                    server_outer_ip = re.get('server_outer_ip')  # 服务器外网ip
                    local_ip = re.get('server_inner_ip')  # 服务器内网ip
                    _res2 = Inner_logic.getInstance().search_service_container_info_list_by_project_id_and_server_id(data={'project_id': project_id, 'server_id': server_id})
                    tomcat_info = []
                    if _res2.is_results_not_none():
                        for service_container_info in _res2.getData():
                            tomcat_info.append({'name': service_container_info.get('service_container_name'), 'port': service_container_info.get('service_container_port')})
                    item = {
                        'data': {
                            'method': 'initProjectConf',
                            'confData': {
                                project_context: {
                                    'project_name': project_name,
                                    'projectHome': project_default_root_path,
                                    'projectType': project_type_code_id,
                                    'upstream_conf_file': upstream_conf_file,
                                    'redis_ip': redis_ip,
                                    'redis_port': redis_port,
                                    'redis_password': redis_password,
                                    'local_ip': local_ip,
                                    'backupConfPath': update_share_conf_bak_path,
                                    'backupFilePath': update_share_bak_path + os.sep + project,
                                    'tomcatInfo': tomcat_info,
                                    'serviceCheckUrl': project_check_service,
                                    'serviceMaxCheckTime': 600,
                                    'tomcatCount': len(tomcat_info),
                                    'maxRestartCount': 3,

                                }
                            }
                        }
                    }
                    # url = agent_service_url.replace('localhost', '192.168.6.252')
                    url = agent_service_url.replace('localhost', server_outer_ip)
                    par = {'url': url, 'json_par': item, 'time_out': 3, 'request_ip': server_outer_ip}
                    po_ins.add_thread(po_ins.pr_post, kwargs=par)
                po_ins.start().join()
                success_ips = []
                success_count = 0
                failed_ips = []
                failed_count = 0
                for re in po_ins.res_queue.queue:
                    if re.is_result_not_none():
                        success_count = success_count + 1
                        success_ips.append(re.getData().get('request_ip'))
                    else:
                        failed_count = failed_count + 1
                        failed_ips.append(re.getData().get('request_ip'))
                result = {
                    'exec_count': (failed_count + success_count),
                    'success_count': success_count,
                    'failed_count': failed_count,
                    'success_ips': success_ips,
                    'failed_ips': failed_ips,
                }
                if failed_count == 0:
                    msg = Msg.getInstance().set_msg('远程重建更新配置文件成功,相关信息为:%s' % str(result)).set_user_name(session_id=__sessionId__).set_par(data).json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1', 'data': result}).setMsg('远程重建更新配置文件成功')
                else:
                    msg = Msg.getInstance().set_msg('远程重建更新配置文件异常,相关信息为:%s' % str(result)).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '0', 'data': result}).setMsg('远程重建更新配置文件,部分成功')
            else:
                msg = Msg.getInstance().set_msg('远程重建更新配置文件,未查询到服务器关联信息').set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_error().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': '0'}).setMsg('远程重建更新配置文件,未查询到服务器关联信息')
        else:
            msg = Msg.getInstance().set_msg('远程重建更新配置文件,未查询到当前项目信息').set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_error().json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': '0'}).setMsg('远程重建更新配置文件,未查询到当前项目信息')


def getInstance():
    return ProjectUpdateConf()
