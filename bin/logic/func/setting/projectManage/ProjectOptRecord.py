#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.data import PostUntil
from bin.base.data import Time
from bin.base.data import Data
from bin.base.sys import Msg
from bin.base.sys import SingleTableOpt
from bin.base.tool import RabbitMQ
from bin.logic import Inner_logic
from bin.logic.BO.OAMP.ProjectOptRecordBo import ProjectOptRecordBo
from bin.logic.func.setting.projectManage import ProjectBaseOpt
from bin.logic.func.setting.projectManage import ProjectOptResultCheck
from bin.logic.func.common import PublishMQFunc
from bin.base.sys.Session import SessionDataOpt
from bin.base.sys import PR
import copy
import os


# 项操作记录
class ProjectOptRecord(object):
    def __init__(self, project_id=None):
        if project_id is not None:
            self.opt_id = Data.getUUID()
            self.project_id = project_id
            project_re = Inner_logic.getInstance().search_project_info_by_id({'project_id': self.project_id})
            project_update_conf_res = Inner_logic.getInstance().search_project_update_conf_info_by_project_id({'project_id': self.project_id})
            if project_re.is_result_not_none():
                self.project_data = project_re.getData()
                self.project = self.project_data.get('project')  # 项目版本信息
                self.project_context = self.project_data.get('project_context')  # 项目版本信息
                self.project_version = self.project_data.get('project_version')  # 项目版本信息
                self.project_last_version = self.project_data.get('project_last_version')  # 项目版本信息
            if project_update_conf_res.is_results_not_none():
                self.project_update_conf_data = project_update_conf_res.getData()[0]
                self.update_path = self.project_update_conf_data.get('update_path')
                self.remark_bak_path = self.project_update_conf_data.get('remark_bak_path')
                self.agent_service_url = self.project_update_conf_data.get('agent_service_url')
                self.update_server_port = self.project_update_conf_data.get('update_server_port')
                self.update_server_ip = self.project_update_conf_data.get('update_server_ip')
                self.update_share_bak_path = self.project_update_conf_data.get('update_share_bak_path')
                self.update_ex_resource = self.project_update_conf_data.get('update_ex_resource')

    def __upload_resource(self, opt_version):
        tar_home_path = self.remark_bak_path + os.sep + self.project
        tar_name = str(opt_version) + '.tar.gz'
        # 此处可能还需要启动一个线程去监听上传进度情况 to fixed 2019年1月23日10:09:21
        return ProjectBaseOpt.getInstance().upload_resource(tar_home_path, tar_name, self.update_server_ip, self.update_server_port, self.update_share_bak_path + os.sep + self.project_context)

    # 标记版本(类 内部使用)
    def __project_remark_version(self, libRes, resourceLibRes, staticFileRes, project_opt_version):
        project_opt_last_version = self.project_version  # 项目版本信息
        return ProjectBaseOpt.getInstance().remark_project(self.project_context, project_opt_version, project_opt_last_version, libRes, resourceLibRes, staticFileRes, self.remark_bak_path, self.update_ex_resource)

    # 启动远程服务
    def __start_remote_service(self, method, project_opt_version):
        po_ins = PostUntil.getInstance()
        server_res = Inner_logic.getInstance().search_server_list_by_project_id({'project_id': self.project_id})
        if server_res.is_results_not_none():
            for server_info in server_res.getData():
                server_outer_ip = server_info.get('server_outer_ip')
                item = {
                    'data': self.__create_remote_service_par(method, project_opt_version),
                    'restartMode': 'one_half',  # single、one_half、whole
                    'method': method,
                }
                url = self.agent_service_url.replace('localhost', server_outer_ip)
                par = {'url': url, 'json_par': item, 'time_out': 3, 'request_ip': server_outer_ip}
                po_ins.add_thread(po_ins.pr_post, kwargs=par)
            po_ins.start().join()
        success_count = 0
        remote_ips = []
        for re in po_ins.res_queue.queue:
            if re.is_result_not_none():
                success_count = success_count + 1
            remote_ips.append(re.getData().get('request_ip'))
        return remote_ips, success_count == len(po_ins.res_queue.queue)

    def __create_remote_service_par(self, method, project_opt_version):
        item = {
            'method': method,
            'opt_id': self.opt_id,
            'projectName': self.project_context,
            'projectVersion': project_opt_version,
        }
        return item

    # 查询项目操作记录信息列表
    def OAMP_search_project_opt_record_info_list(self, data):
        x = {
            'id': data.get('_id'),
            'project_id': data.get('project_id'),
            'project_opt_type_code_id': data.get('project_opt_type_code_id'),
            'is_opt_success': data.get('is_opt_success'),
            'project_opt_version': None if data.get('project_opt_version') is None else str(data.get('project_opt_version')),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(ProjectOptRecordBo).search(filters=x, par=data)

    # 查询id查询项目操作记录
    def OAMP_search_project_opt_record_info_by_id(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectOptRecordBo).setData(data=data).search()

    # 插入项目操作记录信息
    def OAMP_insert_project_opt_record_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectOptRecordBo).setData(data=data).insert()

    # 更新项目操作记录信息
    def OAMP_update_project_opt_record_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectOptRecordBo).setData(data=data).update()

    # 更新项目操作记录信息
    def OAMP_delete_project_opt_record_info(self, data):
        return SingleTableOpt.getInstance().setBO(ProjectOptRecordBo).setData(data=data).delete()

    # 标记版本
    def _project_remark_version(self, data):
        libRes = data.get('libRes')
        resourceLibRes = data.get('resourceLibRes')
        staticFileRes = data.get('staticFileRes')
        project_opt_version = data.get('project_opt_version')
        project_opt_last_version = self.project_version  # 项目版本信息
        remark_result = ProjectBaseOpt.getInstance().remark_project(self.project_context, project_opt_version, project_opt_last_version, libRes, resourceLibRes, staticFileRes, self.remark_bak_path, self.update_ex_resource)
        if remark_result:
            return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('标记项目成功')
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('标记项目失败')

    # 上传资源
    def _upload_resource(self, opt_version):
        tar_home_path = self.remark_bak_path + os.sep + self.project_context
        tar_name = str(opt_version) + '.tar.gz'
        return ProjectBaseOpt.getInstance().upload_resource(tar_home_path, tar_name, self.update_server_ip, self.update_server_port, self.update_share_bak_path + os.sep + self.project_context)

    # 静态文件更新
    def _project_static_file_update(self, data, method='replaceResource'):
        project_opt_version = data.get('project_opt_version')
        remark_version_re = self._project_remark_version(data=data)
        if remark_version_re.getCode() == PR.Code_OK:  # 标记版本操作完成
            if self._upload_resource(project_opt_version):
                success_ips = []
                success_count = 0
                failed_ips = []
                failed_count = 0
                po_ins = PostUntil.getInstance()
                server_res = Inner_logic.getInstance().search_server_list_by_project_id({'project_id': self.project_id})
                if server_res.is_results_not_none():
                    for server_info in server_res.getData():
                        server_outer_ip = server_info.get('server_outer_ip')
                        item = {
                            'data': {
                                'method': method,
                                'projectName': self.project_context,
                                'projectVersion': project_opt_version,
                                'opt_id': self.opt_id
                            }
                        }
                        url = self.agent_service_url.replace('localhost', server_outer_ip)
                        par = {'url': url, 'json_par': item, 'time_out': 3, 'request_ip': server_outer_ip}
                        po_ins.add_thread(po_ins.pr_post, kwargs=par)
                    po_ins.start().join()
                for re in po_ins.res_queue.queue:
                    if re.is_result_not_none():
                        success_count = success_count + 1
                        success_ips.append(re.getData().get('request_ip'))
                    else:
                        failed_count = failed_count + 1
                        failed_ips.append(re.getData().get('request_ip'))
                result = {
                    'exec_count': (failed_count + success_count),
                    'exec_ips': success_ips + failed_ips,
                    'success_count': success_count,
                    'success_ips': success_ips,
                    'failed_count': failed_count,
                    'failed_ips': failed_ips,
                }
                return PR.getInstance().setCode(PR.Code_OK).setData(result).setMsg('资源替换操作成功')
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('标记项目失败')

    # 项目更新
    def _project_update(self, data, method='updateProject'):
        remark_re = self._project_remark_version(data)
        if remark_re.getCode() == PR.Code_OK:
            project_opt_version = data.get('project_opt_version')
            if self._upload_resource(project_opt_version):
                success_ips = []
                success_count = 0
                failed_ips = []
                failed_count = 0
                po_ins = PostUntil.getInstance()
                server_res = Inner_logic.getInstance().search_server_list_by_project_id({'project_id': self.project_id})
                if server_res.is_results_not_none():
                    for server_info in server_res.getData():
                        server_outer_ip = server_info.get('server_outer_ip')
                        item = {
                            'data': {
                                'method': method,
                                'projectName': self.project_context,
                                'projectVersion': project_opt_version,
                                'opt_id': self.opt_id,
                                'restartMode': 'one_half'  # single、one_half、whole
                            }
                        }
                        url = self.agent_service_url.replace('localhost', server_outer_ip)
                        par = {'url': url, 'json_par': item, 'time_out': 3, 'request_ip': server_outer_ip}
                        po_ins.add_thread(po_ins.pr_post, kwargs=par)
                    po_ins.start().join()
                for re in po_ins.res_queue.queue:
                    if re.is_result_not_none():
                        success_count = success_count + 1
                        success_ips.append(re.getData().get('request_ip'))
                    else:
                        failed_count = failed_count + 1
                        failed_ips.append(re.getData().get('request_ip'))
                result = {
                    'exec_count': (failed_count + success_count),
                    'exec_ips': success_ips + failed_ips,
                    'success_count': success_count,
                    'success_ips': success_ips,
                    'failed_count': failed_count,
                    'failed_ips': failed_ips,
                }
                return PR.getInstance().setCode(PR.Code_OK).setData(result).setMsg('更新项目操作成功')
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('更新项目，上传资源失败')
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setMsg('更新项目，标记项目失败')

    # 获取项目标记插入信息bean对象
    def __create_project_remark_opt_record_item(self, data):
        item = {
            '_id': self.opt_id,
            'project_id': self.project_id,
            'project_opt_user_name': SessionDataOpt(sessionId=data.get('__sessionId__')).getUserName(),
            'project_opt_version': str(data.get('project_opt_version')),
            'project_opt_summary': '%s项目%s版本标记' % (str(self.project_context), str(data.get('project_opt_version'))),
            'project_opt_last_version': str(self.project_version),
            'project_opt_type_code_id': '2',  # 标记项目
            'project_opt_res_info': [{'libRes': data.get('libRes')}, {'ResourceLibRes': data.get('resourceLibRes')}, {'staticFileRes': data.get('staticFileRes')}],
            'project_opt_start_time': Time.get_create_time(),
            'exec_state_code_id': '4',  # 无需执行
            'is_opt_success': '',
            'is_able_rollback': '0',
        }
        return item

    # 当前最优实现方案，将请求发送到MQ中，使用MQ进行执行方法，实现上传然后回调
    # 标记版本信息
    def OAMP_project_remark_version(self, data):
        try:
            __sessionId__ = data.get('__sessionId__')
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            insert_record_bean = self.__create_project_remark_opt_record_item(data=data)
            insert_re = self.OAMP_insert_project_opt_record_info(data=insert_record_bean)  # 插入标记项目操作记录信息
            res_re = self._project_remark_version(data=data)
            if res_re.getCode() == PR.Code_OK and insert_re.getCode() == PR.Code_OK:
                update_bean = copy.copy(self.project_data)
                update_bean['project_version'] = str(project_opt_version)
                update_bean['project_last_version'] = str(self.project_version)
                update_bean['project_last_opt_summary'] = project_opt_summary
                u_re = Inner_logic.getInstance().update_project_info(data=update_bean)  # 修改项目版本信息
                update_record_bean = copy.copy(insert_re.getData())
                update_record_bean['project_opt_end_time'] = Time.get_update_time()
                # update_record_bean['exec_state_code_id'] = '4'  # 无需执行
                update_record_bean['is_opt_success'] = '1'
                update_re = self.OAMP_update_project_opt_record_info(data=update_record_bean)  # 修改标记项目操作记录信息
                if u_re.getCode() == PR.Code_OK and update_re.getCode() == PR.Code_OK:
                    msg = Msg.getInstance().set_msg('标记%s项目%s版本成功' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_par(data).json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                else:
                    msg = Msg.getInstance().set_msg('标记%s项目%s版本成功,修改相关信息失败' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return res_re
            else:
                msg = Msg.getInstance().set_msg('标记%s项目%s版本失败' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_error().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('标记版本错误:%s' % str(res_re.getMsg()))
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setMsg('标记版本异常:' + str(e))

    def __create_project_increase_update_opt_record_item(self, data):
        item = {
            '_id': self.opt_id,
            'project_id': self.project_id,
            'project_opt_user_name': SessionDataOpt(sessionId=data.get('__sessionId__')).getUserName(),
            'project_opt_version': str(data.get('project_opt_version')),
            'project_opt_summary': '%s项目%s版本增量更新' % (str(self.project_context), str(data.get('project_opt_version'))),
            'project_opt_last_version': str(self.project_version),
            'project_opt_type_code_id': '6',  # 增量更新
            'project_opt_res_info': [{'libRes': data.get('libRes')}, {'ResourceLibRes': data.get('resourceLibRes')}, {'staticFileRes': data.get('staticFileRes')}],
            'project_opt_start_time': Time.get_create_time(),
            'exec_state_code_id': '0',  # 0 未执行
            'is_opt_success': '',
            'is_able_rollback': '0',
        }
        return item

    # 增量更新
    def OAMP_project_increase_update(self, data):
        try:
            __sessionId__ = data.get('__sessionId__')
            data['opt_id'] = self.opt_id
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            insert_opt_record_item = self.__create_project_increase_update_opt_record_item(data=data)
            insert_record_re = self.OAMP_insert_project_opt_record_info(data=insert_opt_record_item)  # 添加操作记录
            if insert_record_re.getCode() == PR.Code_OK:
                msg = Msg.getInstance().set_msg('发布[%s]项目%s版本增量更新服务' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_type_project_inc_update().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                PublishMQFunc.getInstance().set_project(self.project_context).set_par(data).set_user_name(session_id=__sessionId__).set_method('MQ_project_increase_update').publish()

                project_u_bean = copy.copy(self.project_data)
                project_u_bean['project_last_opt_summary'] = project_opt_summary
                project_u_bean['project_state_code_id'] = 'INCREASE_UPDATE'  # 增量更新中
                Inner_logic.getInstance().update_project_info(project_u_bean)  # 修改项目信息 把项目更改为执行中状态

                return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('项目增量更新操作成功')
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('生成项目增量更新记录错误')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setMsg('项目增量更新过程异常:%s' % str(e))

    # 增量更新 MQ
    def MQ_project_increase_update(self, data):
        # 1、 解析参数
        self.opt_id = data.get('opt_id')
        record_re = Inner_logic.getInstance().search_project_opt_record_info_by_id({'_id': self.opt_id})
        record_data = record_re.getData()
        record_data['exec_state_code_id'] = '1'  # 1 执行中
        Inner_logic.getInstance().update_project_opt_record_info(data=record_data)  # 更改操作记录为执行中

        project_opt_version = data.get('project_opt_version')
        libRes = data.get('libRes')
        resourceLibRes = data.get('resourceLibRes')
        staticFileRes = data.get('staticFileRes')
        __sessionId__ = data.get('__sessionId__')
        # 标记项目
        remark_result = self.__project_remark_version(libRes, resourceLibRes, staticFileRes, project_opt_version)
        if remark_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 上传项目
        upload_result = self.__upload_resource(opt_version=project_opt_version)
        if upload_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 启动远程服务
        exec_ips, service_result = self.__start_remote_service(method='updateProject', project_opt_version=project_opt_version)
        if service_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 获取服务结果
        user_name = SessionDataOpt(sessionId=__sessionId__).getUserName()
        start_check_result = ProjectOptResultCheck.getInstance().start_opt_result_check(user_name=user_name, ips=exec_ips, opt_id=self.opt_id, project_name=self.project_context, service_name='项目增量更新', service_url=self.agent_service_url)  # 启动操作结果检查
        if start_check_result:
            pass  # 修改过程记录
        else:
            return False

        return True

    def __create_project_full_update_opt_record_item(self, data):
        item = {
            '_id': self.opt_id,
            'project_id': self.project_id,
            'project_opt_user_name': SessionDataOpt(sessionId=data.get('__sessionId__')).getUserName(),
            'project_opt_version': str(data.get('project_opt_version')),
            'project_opt_summary': '%s项目%s版本全量更新' % (str(self.project_context), str(data.get('project_opt_version'))),
            'project_opt_last_version': str(self.project_version),
            'project_opt_type_code_id': '5',  # 标记项目
            'project_opt_res_info': [{'libRes': data.get('libRes')}, {'ResourceLibRes': data.get('resourceLibRes')}, {'staticFileRes': data.get('staticFileRes')}],
            'project_opt_start_time': Time.get_create_time(),
            'exec_state_code_id': '0',  # 0 未执行
            'is_opt_success': '',
            'is_able_rollback': '0',
        }
        return item

    # 全量更新
    def OAMP_project_full_update(self, data):
        try:
            __sessionId__ = data.get('__sessionId__')
            data['opt_id'] = self.opt_id
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            insert_opt_record_item = self.__create_project_full_update_opt_record_item(data=data)
            insert_record_re = self.OAMP_insert_project_opt_record_info(data=insert_opt_record_item)  # 添加操作记录
            if insert_record_re.getCode() == PR.Code_OK:
                msg = Msg.getInstance().set_msg('发布[%s]项目%s版本全量更新服务' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_type_project_full_update().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

                pub_ins = PublishMQFunc.getInstance()
                pub_ins.set_project(self.project_context).set_par(data)
                pub_ins.set_user_name(session_id=__sessionId__)
                pub_ins.set_method('MQ_project_full_update').publish()

                project_u_bean = copy.copy(self.project_data)
                project_u_bean['project_last_opt_summary'] = project_opt_summary
                project_u_bean['project_state_code_id'] = 'FULL_UPDATE'  # 全量更新中
                Inner_logic.getInstance().update_project_info(project_u_bean)  # 修改项目信息 把项目更改为执行中状态

                return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('项目全量更新操作成功')
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('生成项目全量更新记录错误')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setMsg('项目全量更新过程异常:%s' % str(e))

    # 全量更新MQ
    def MQ_project_full_update(self, data):
        # 1、 解析参数
        self.opt_id = data.get('opt_id')
        record_re = Inner_logic.getInstance().search_project_opt_record_info_by_id({'_id': self.opt_id})
        record_data = record_re.getData()
        record_data['exec_state_code_id'] = '1'  # 1 执行中
        Inner_logic.getInstance().update_project_opt_record_info(data=record_data)  # 更改操作记录为执行中

        project_opt_version = data.get('project_opt_version')
        libRes = data.get('libRes')
        resourceLibRes = data.get('resourceLibRes')
        staticFileRes = data.get('staticFileRes')
        __sessionId__ = data.get('__sessionId__')
        # 标记项目
        remark_result = self.__project_remark_version(libRes, resourceLibRes, staticFileRes, project_opt_version)
        if remark_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 上传项目
        upload_result = self.__upload_resource(opt_version=project_opt_version)
        if upload_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 启动远程服务
        exec_ips, service_result = self.__start_remote_service(method='updateProject', project_opt_version=project_opt_version)
        if service_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 获取服务结果
        user_name = SessionDataOpt(sessionId=__sessionId__).getUserName()
        start_check_result = ProjectOptResultCheck.getInstance().start_opt_result_check(user_name=user_name, ips=exec_ips, opt_id=self.opt_id, project_name=self.project_context, service_name='项目全量更新', service_url=self.agent_service_url)  # 启动操作结果检查
        if start_check_result:
            pass  # 修改过程记录
        else:
            return False

        return True

    # 标记更新
    def OAMP_project_remark_update(self, data):
        # to fixed 2019年3月4日12:06:13
        try:
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            pass
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult(None).setMsg('项目标记更新过程异常:%s' % str(e))

        try:
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            res_re = self._project_update(data=data)
            __sessionId__ = data.get('__sessionId__')
            if res_re.getCode() == PR.Code_OK:
                res_data = res_re.getData()
                if res_data.get('failed_count') == 0:
                    update_bean = copy.copy(self.project_data)
                    update_bean['project_version'] = str(project_opt_version)
                    update_bean['project_last_version'] = str(self.project_version)
                    update_bean['project_last_opt_summary'] = project_opt_summary
                    u_re = Inner_logic.getInstance().update_project_info(data=update_bean)
                    if u_re.getCode() == PR.Code_OK:
                        msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记更新成功,相关信息为:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).json()
                        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    else:
                        msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记更新异常,项目更新版本信息错误:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setData(res_data).setMsg('项目标记更新成功')
                else:
                    msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记更新异常,部分服务器异常,相关信息为:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '0'}).setData(res_data).setMsg('项目标记更新异常')
            else:
                msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记更新失败' % (str(self.project_context), str(self.project_version))).set_user_name(session_id=__sessionId__).set_msg_level_error().set_par(data).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('执行项目标记更新过程错误:%s' % str(res_re.getMsg()))
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult(None).setMsg('项目标记更新过程异常:%s' % str(e))

    # 标记取消
    def OAMP_project_remark_cancel(self, data):
        pass
        # # 1、操作记录修改为标记取消
        # # 2、项目最新版本 变更？ 取消之后的版本
        # update_bean = copy.copy(self.project_data)
        # update_bean['project_opt_type_code_id'] = '8'  # 标记取消
        # u_re = Inner_logic.getInstance().update_project_info(data=update_bean)
        # if u_re.getCode() == PR.Code_OK:
        #     msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记取消成功,执行信息为:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).json()
        #     RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        # else:
        #     msg = Msg.getInstance().set_msg('执行%s项目%s版本项目标记取消异常,错误信息:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
        #     RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

    # 项目回滚
    def OAMP_project_roll_back_update(self, data):
        try:
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            res_re = self._project_update(data=data)
            __sessionId__ = data.get('__sessionId__')
            if res_re.getCode() == PR.Code_OK:
                res_data = res_re.getData()
                if res_data.get('failed_count') == 0:
                    update_bean = copy.copy(self.project_data)
                    update_bean['project_version'] = str(project_opt_version)
                    update_bean['project_last_version'] = str(self.project_version)
                    update_bean['project_last_opt_summary'] = project_opt_summary
                    u_re = Inner_logic.getInstance().update_project_info(data=update_bean)
                    if u_re.getCode() == PR.Code_OK:
                        msg = Msg.getInstance().set_msg('执行%s项目%s版本项目回滚更新成功,相关信息为:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).json()
                        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    else:
                        msg = Msg.getInstance().set_msg('执行%s项目%s版本项目回滚更新异常,项目更新版本信息错误:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setData(res_data).setMsg('项目回滚更新成功')
                else:
                    msg = Msg.getInstance().set_msg('执行%s项目%s版本项目回滚更新异常,部分服务器异常,相关信息为:%s' % (str(self.project_context), str(self.project_version), str(res_data))).set_user_name(session_id=__sessionId__).set_par(data).set_msg_level_exception().json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '0'}).setData(res_data).setMsg('项目回滚更新异常')
            else:
                msg = Msg.getInstance().set_msg('执行%s项目%s版本项目回滚更新失败' % (str(self.project_context), str(self.project_version))).set_user_name(session_id=__sessionId__).set_msg_level_error().set_par(data).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('执行项目回滚更新过程错误:%s' % str(res_re.getMsg()))
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult(None).setMsg('项目回滚更新过程异常:%s' % str(e))

    # 静态文件更新
    # 1、将参数封装
    # 2、发送消息进入MQ中
    # 3、添加操作记录
    # 4、返回成功
    def __create_project_static_file_update_opt_record_item(self, data):  #
        item = {
            '_id': self.opt_id,
            'project_id': self.project_id,
            'project_opt_user_name': SessionDataOpt(sessionId=data.get('__sessionId__')).getUserName(),
            'project_opt_version': str(data.get('project_opt_version')),
            'project_opt_summary': '%s项目%s版本资源替换' % (str(self.project_context), str(data.get('project_opt_version'))),
            'project_opt_last_version': str(self.project_version),
            'project_opt_type_code_id': '3',  # 3资源替换
            'project_opt_res_info': [{'libRes': data.get('libRes')}, {'ResourceLibRes': data.get('resourceLibRes')}, {'staticFileRes': data.get('staticFileRes')}],
            'project_opt_start_time': Time.get_create_time(),
            'exec_state_code_id': '0',  # 0 未执行
            'is_opt_success': '',
            'is_able_rollback': '0',
        }
        return item

    # 项目静态文件更新操作 web 触发
    def OAMP_project_static_file_update(self, data):
        try:
            __sessionId__ = data.get('__sessionId__')
            data['opt_id'] = self.opt_id
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            insert_opt_record_item = self.__create_project_static_file_update_opt_record_item(data=data)
            insert_record_re = self.OAMP_insert_project_opt_record_info(data=insert_opt_record_item)  # 添加操作记录
            if insert_record_re.getCode() == PR.Code_OK:
                msg = Msg.getInstance().set_msg('发布[%s]项目%s版本静态文件更新服务' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_type_project_res_upload().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                pub_ins = PublishMQFunc.getInstance()
                pub_ins.set_project(self.project_context).set_par(data)
                pub_ins.set_user_name(session_id=__sessionId__)
                pub_ins.set_method('MQ_project_static_file_update').publish()

                project_u_bean = copy.copy(self.project_data)
                project_u_bean['project_last_opt_summary'] = project_opt_summary
                project_u_bean['project_state_code_id'] = 'REPLACE_RES'  # 替换资源中
                Inner_logic.getInstance().update_project_info(project_u_bean)  # 修改项目信息 把项目更改为执行中状态

                return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('静态文件更新操作成功')
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('生成静态文件更新记录错误')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setMsg('静态文件更新过程异常:%s' % str(e))

    # 项目静态文件更新操作 MQ 触发
    def MQ_project_static_file_update(self, data):
        # 1、 解析参数
        self.opt_id = data.get('opt_id')
        record_re = Inner_logic.getInstance().search_project_opt_record_info_by_id({'_id': self.opt_id})
        record_data = record_re.getData()
        record_data['exec_state_code_id'] = '1'  # 1 执行中
        Inner_logic.getInstance().update_project_opt_record_info(data=record_data)  # 更改操作记录为执行中

        project_opt_summary = data.get('project_opt_summary')
        project_opt_version = data.get('project_opt_version')
        libRes = data.get('libRes')
        resourceLibRes = data.get('resourceLibRes')
        staticFileRes = data.get('staticFileRes')
        __sessionId__ = data.get('__sessionId__')
        # 标记项目
        remark_result = self.__project_remark_version(libRes, resourceLibRes, staticFileRes, project_opt_version)
        if remark_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 上传项目
        upload_result = self.__upload_resource(opt_version=project_opt_version)
        if upload_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 启动远程服务
        exec_ips, service_result = self.__start_remote_service(method='replaceResource', project_opt_version=project_opt_version)
        if service_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 获取服务结果
        user_name = SessionDataOpt(sessionId=__sessionId__).getUserName()
        start_check_result = ProjectOptResultCheck.getInstance().start_opt_result_check(user_name=user_name, ips=exec_ips, opt_id=self.opt_id, project_name=self.project_context, service_name='项目静态文件更新', service_url=self.agent_service_url)  # 启动操作结果检查
        if start_check_result:
            pass  # 修改过程记录
        else:
            return False

        return True

    # 获取项目重启插入信息bean对象
    def __create_project_restart_opt_record_item(self, data):
        item = {
            '_id': self.opt_id,
            'project_id': self.project_id,
            'project_opt_user_name': SessionDataOpt(sessionId=data.get('__sessionId__')).getUserName(),
            'project_opt_version': str(self.project_version),
            'project_opt_summary': '%s项目%s版本进行项目重启操作' % (str(self.project_context), str(self.project_version)),
            'project_opt_last_version': str(self.project_last_version),
            'project_opt_type_code_id': '1',  # 1重启
            'project_opt_start_time': Time.get_create_time(),
            'exec_state_code_id': '0',  # 0 未执行
            'is_opt_success': '',
            'is_able_rollback': '0',
        }
        return item

    # 项目重启
    def OMAP_project_restart(self, data):
        try:
            __sessionId__ = data.get('__sessionId__')
            data['opt_id'] = self.opt_id
            project_opt_summary = data.get('project_opt_summary')
            project_opt_version = data.get('project_opt_version')
            insert_opt_record_item = self.__create_project_restart_opt_record_item(data=data)
            insert_record_re = self.OAMP_insert_project_opt_record_info(data=insert_opt_record_item)  # 添加操作记录
            if insert_record_re.getCode() == PR.Code_OK:
                msg = Msg.getInstance().set_msg('发布[%s]项目%s版本重启服务' % (self.project_context, str(project_opt_version))).set_user_name(session_id=__sessionId__).set_type_project_restart().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

                pub_ins = PublishMQFunc.getInstance()
                pub_ins.set_project(self.project_context).set_par(data)
                pub_ins.set_user_name(session_id=__sessionId__)
                pub_ins.set_method('MQ_project_restart').publish()

                project_u_bean = copy.copy(self.project_data)
                project_u_bean['project_last_opt_summary'] = project_opt_summary
                project_u_bean['project_state_code_id'] = 'RESTART'  # 重启中
                Inner_logic.getInstance().update_project_info(project_u_bean)  # 修改项目信息 把项目更改为执行中状态

                return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': '1'}).setMsg('项目重启操作成功')
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setMsg('生成项目重启记录错误')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setMsg('项目重启过程异常:%s' % str(e))

    # 项目重启 MQ
    def MQ_project_restart(self, data):
        # 1、 解析参数
        self.opt_id = data.get('opt_id')
        record_re = Inner_logic.getInstance().search_project_opt_record_info_by_id({'_id': self.opt_id})
        record_data = record_re.getData()
        record_data['exec_state_code_id'] = '1'  # 1 执行中
        Inner_logic.getInstance().update_project_opt_record_info(data=record_data)  # 更改操作记录为执行中

        project_opt_version = data.get('project_opt_version')
        __sessionId__ = data.get('__sessionId__')
        # 启动远程服务
        exec_ips, service_result = self.__start_remote_service(method='restartProject', project_opt_version=project_opt_version)
        if service_result:
            pass  # 修改过程记录 进度
        else:
            return False
        # 获取服务结果
        user_name = SessionDataOpt(sessionId=__sessionId__).getUserName()
        project_opt_check_ins = ProjectOptResultCheck.getInstance()
        service_name = '%s项目%s版本重启' % (str(self.project_context), str(project_opt_version))
        start_check_result = project_opt_check_ins.start_opt_result_check(user_name=user_name, ips=exec_ips, opt_id=self.opt_id, project_name=self.project_context, service_name=service_name, service_url=self.agent_service_url)  # 启动操作结果检查
        if start_check_result:
            pass  # 修改过程记录
        else:
            return False
        return True


def getInstance(project_id=None):
    return ProjectOptRecord(project_id)
