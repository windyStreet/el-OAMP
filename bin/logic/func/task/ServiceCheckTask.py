# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.sys import Msg
from bin.base.sys import SingleTableOpt
from bin.base.sys import PR
from bin.base.log import Logger
from bin.base.tool import RabbitMQ
from bin.base.tool import Redis
from bin.logic.func.task import ApschedulerTaskFunc
from bin.logic.func.common import Link
from bin.logic.BO.OAMP.ServiceCheckBo import ServiceCheckBo
from bin.logic.BO.OAMP.ServiceContainerBo import ServiceContainerBo
from bin.logic.BO.OAMP.ServerBo import ServerBo
from bin.logic.BO.OAMP.ProjectBo import ProjectBo
from bin.base.data import PostUntil
import threading

L = Logger.getInstance('ServiceCheck.log')
R = Redis.getInstance(ds=init.ROOT_REDIS_DS, db=init.DEFAULT_SERVICE_CHECK_REDIS_DB)


class ServiceCheckTask(object):
    def __init__(self):
        pass

    # 检查服务
    def _check_post_service(self, service_check_info, is_manual=False):
        _id = service_check_info.get('_id')
        service_check_url = service_check_info.get('service_check_url')
        service_check_result = service_check_info.get('service_check_result')
        po_ins = PostUntil.getInstance()
        for url in service_check_url:
            par = {'url': url, 'time_out': 2, 'except_res': service_check_result}
            po_ins.add_thread(po_ins.str_post, kwargs=par)
        po_ins.start().join()
        is_success = False
        for re in po_ins.res_queue.queue:
            is_success = re.is_result_not_none()
            if is_success:
                break
        item = self._handle_service_result(key=_id, is_success=is_success)
        self._judge_service(key=_id, item=item, is_manual=is_manual)
        return True

    # 处理检查结果
    def _handle_service_result(self, key, is_success):

        item = self._get_run_service_cehck_info(data={"_id": key})
        if item is None:
            item = {}
        else:
            item['service_check_count'] = item.get('service_check_count') + 1
            if is_success:
                item['service_check_last_result'] = '检测成功'  # 服务检查最后一次运行结果
                item['service_check_continued_error_count'] = 0  # 检查错误持续次数置0
                item['service_state_code_id'] = '1'  # 服务运行状态 运行中
            else:
                item['service_check_last_result'] = '检测失败'  # 服务检查最后一次运行结果
                item['service_check_error_count'] = item.get('service_check_error_count') + 1  # 发生错误的次数
                item['service_check_continued_error_count'] = item.get('service_check_continued_error_count') + 1  # 发生错误的次数
                item['service_state_code_id'] = '2'  # 服务运行状态 运行异常
        return item

    # 判断检查结果
    def _judge_service(self, key, item, is_manual):
        service_check_threshold = item.get('service_check_threshold', 3)
        r_item = R.getJson(key=key)
        if (r_item.get('service_check_continued_error_count') is not item.get('service_check_continued_error_count') and item.get('service_check_continued_error_count') < 20) or item.get('service_check_count') % 5 is 1 or is_manual is True:
            L.info('服务检查任务定时修改数据库，data:' + str(item))
            # 在错误20次以内,服务检查错误结果变化
            # 每5分钟记录一次数据库
            # 改数据库
            SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=item).update()
        if r_item.get('service_check_continued_error_count') >= service_check_threshold and item.get('service_check_continued_error_count') is 0:
            # 好像是服务恢复了，大吉大利，发个邮件庆祝下
            L.info('好像是服务恢复了，大吉大利，发个邮件庆祝下')
            # 还需要去修改项目状态
            L.info('发送一个MQ 消息，通知更新项目运行状态吧')
            SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=item).update()
            msg = Msg.getInstance().set_msg('发布[%s]项目[%s]服务变更任务,服务恢复' % (item.get('service_name'), item.get('_id'))).set_type_project_service_check().set_par(r_item).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        if service_check_threshold <= item.get('service_check_continued_error_count') < service_check_threshold + 2:
            L.info('好像服务出现了问题,发个邮件，最多发两次就行了')
            L.info('发送一个MQ 消息，通知更新项目运行状态吧')
            # 还需要去修改项目状态
            SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=item).update()
            msg = Msg.getInstance().set_msg('发布[%s]项目[%s]服务变更任务,服务故障' % (item.get('service_name'), item.get('_id'))).set_type_project_service_check().set_par(r_item).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        if item.get('service_check_continued_error_count') % 60 is service_check_threshold:
            L.info('服务出现问题，半天了，该处理了')
            L.info('再发个邮件催一催')
        R.setJson(key=key, value=item, ex=300)

    # 添加服务检查
    # service_check 对象
    def _add_service_check(self, service_check_info, data):
        __sessionId__ = data.get('__sessionId__', 'sys')
        ins = ApschedulerTaskFunc.getInstance(task_type= init.APS_TASKS.get('SERVICE_CHECK')).get_scheduler_ins()

        _id = service_check_info.get('_id')
        seconds = service_check_info.get('service_check_rate', 60)
        ins.scheduler.add_job(self._check_post_service, args=[service_check_info], id=_id, trigger='interval', seconds=seconds, replace_existing=True, jobstore='mongo')
        msg = Msg.getInstance().set_msg('添加serviceCheck任务成功:[' + service_check_info.get('service_name') + ']').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(service_check_info).json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('add service check success')

    # 删除所有的服务检查
    def _delete_service_check(self, data):
        try:
            x = {'service_project_id': data.get('service_project_id')}
            count_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, par={'pageSize': 1}, only=['id'])
            count = count_res.getPageCount()
            if count > 0:
                page_size = 20
                for i in range(1, int(count / page_size + 2)):
                    service_check_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, par={'pageSize': page_size})
                    if service_check_res.is_results_not_none():
                        for service_check_info in service_check_res.getData():
                            # 1、删除 aps 任务
                            item = {
                                '__sessionId__': data.get('__sessionId__', None),
                                '_id': service_check_info.get('_id', None)
                            }
                            ApschedulerTaskFunc.getInstance(task_type= init.APS_TASKS.get('SERVICE_CHECK')).remove_apscheduler_task(item)
                            # 2、删除服务检查
                            SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(service_check_info).delete()
                return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('删除服务检查任务成功')
            else:
                return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('未发现需要删除的服务检查任务')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('删除的服务检查任务出现异常:' + str(e))

    # 生成服务检查数据
    def _create_service_check_data(self, data):
        # 1、查询所有项目
        x = {
            'id': data.get('service_project_id', None),
            'project_state_code_id': 'RUNNING',
        }
        count_res = SingleTableOpt.getInstance().setBO(ProjectBo).search(filters=x, par={'pageSize': 1}, only=['id'])
        count = count_res.getPageCount()
        if count > 0:
            page_size = 20
            for i in range(1, int(count / page_size + 2)):
                _project_res = SingleTableOpt.getInstance().setBO(ProjectBo).search(filters=x, par={'pageSize': page_size})
                if _project_res.is_results_not_none():
                    for project_info in _project_res.getData():
                        project_name = project_info.get('project_name', None)
                        project_check_result = project_info.get('project_check_result', None)
                        project_check_service = project_info.get('project_check_service', None)
                        if project_check_service is None:  # 没有配置检查地址
                            continue
                        project_id = project_info.get('_id')
                        _project_server_container_res = Link.getInstance().OAMP_search_link_info_by_link_id({'link_id': project_id, 'link_type_code_id': '2'})  # 项目服务容器
                        servers_info = {}
                        _project_server_res = Link.getInstance().OAMP_search_link_info_by_link_id({'link_id': project_id, 'link_type_code_id': '1'})
                        if _project_server_res.is_results_not_none():  # _project_server_res.getCode() == PR.Code_OK and _project_server_res.getData() is not None and len(_project_server_res.getData()) > 0:
                            for _project_server_info in _project_server_res.getData():
                                server_id = _project_server_info.get('linked_id')
                                server_info_res = SingleTableOpt.getInstance().setBO(ServerBo).setData({'_id': server_id}).search()
                                if server_info_res.is_result_not_none():  # server_info_res.getCode() == PR.Code_OK and server_info_res.getData() is not None:
                                    servers_info[server_id] = server_info_res.getData()
                        else:  # 没有发现关联服务器
                            continue
                        if _project_server_container_res.is_results_not_none():  # _project_server_container_res.getCode() == PR.Code_OK and _project_server_container_res.getData() is not None and len(_project_server_container_res.getData()) > 0:
                            for project_server_container_info in _project_server_container_res.getData():
                                service_container_id = project_server_container_info.get('linked_id')
                                # 查询容器信息
                                _service_container_re = SingleTableOpt.getInstance().setBO(ServiceContainerBo).setData({'_id': service_container_id}).search()
                                if _service_container_re.is_result_not_none():  # _service_container_re.getCode() == PR.Code_OK and _service_container_re.getData() is not None:  # 服务容器存在,查找服务器信息
                                    server_ips = []
                                    urls = []
                                    service_container_info = _service_container_re.getData()
                                    server_id = service_container_info.get('belong_to_server_id')
                                    if server_id in servers_info.keys():
                                        server_ips.append(servers_info.get(server_id).get('server_outer_ip', None))
                                        server_ips.append(servers_info.get(server_id).get('server_inner_ip', None))
                                    service_container_port = service_container_info.get('service_container_port')
                                    for server_ip in server_ips:
                                        if server_ip is None:
                                            continue
                                        url = 'http://' + server_ip + ':' + service_container_port + '/' + project_check_service
                                        urls.append(url)
                                    if len(urls) > 0:
                                        service_check_rate = 60
                                        service_check_count = 0
                                        service_check_continued_error_count = 0
                                        service_check_error_count = 0
                                        service_check_threshold = 3
                                        old_item = self._get_run_service_cehck_info({'_id': service_container_id})
                                        if old_item is not None:
                                            service_check_rate = old_item.get('service_check_rate', 60)
                                            service_check_count = old_item.get('service_check_count', 0)
                                            service_check_continued_error_count = old_item.get('service_check_continued_error_count', 0)
                                            service_check_error_count = old_item.get('service_check_error_count', 0)
                                            service_check_threshold = old_item.get('service_check_threshold', 3)
                                        item = {
                                            '_id': service_container_id,
                                            'service_project_id': project_id,
                                            'service_container_id': service_container_id,  # 该结果也是唯一的
                                            'service_name': project_name + '服务检查',
                                            'service_ips': server_ips,
                                            'service_port': service_container_port,
                                            'service_check_rate': service_check_rate,
                                            'service_check_url': urls,
                                            'service_check_result': project_check_result,
                                            'service_check_count': service_check_count,
                                            'service_check_continued_error_count': service_check_continued_error_count,
                                            'service_check_error_count': service_check_error_count,
                                            'service_check_threshold': service_check_threshold,
                                            'service_check_state_code_id': '1'
                                        }
                                        insert_re = SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=item).insert()
                                        if insert_re.is_result_not_none():
                                            self._add_service_check(insert_re.getData(), data)
                        else:  # 没有发现关联服务容器
                            continue
                    return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('操作成功')
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('未查询到项目信息')

    def _get_run_service_cehck_info(self, data):
        item = R.getJson(key=data.get('_id'))
        if item is None:
            re = SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=data).search()
            if re.is_result_not_none():
                item = re.getData()
                R.setJson(key=data.get('_id'), value=item, ex=300)
        return item

    # 重新生成服务检查 data = {'service_project_id':xx}
    def OAMP_recreate_service_check(self, data):
        res_1 = self._delete_service_check(data=data)
        res_2 = self._create_service_check_data(data=data)
        if res_1.getCode() == PR.Code_OK and res_2.getCode() == PR.Code_OK:
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('重新生成服务检查成功')
        else:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('重新生成服务检查异常，请检查代码')

    # 暂停服务检查
    def OAMP_pause_service_check(self, data):
        try:
            item = self._get_run_service_cehck_info(data=data)
            item['service_check_state_code_id'] = '2'  # 暂停状态
            self._update_service_check_info(data=item)
            ApschedulerTaskFunc.getInstance(task_type= init.APS_TASKS.get('SERVICE_CHECK')).pause_apscheduler_task(data=data)
            msg = Msg.getInstance().set_msg('发布[%s]项目服务[%s]变更任务,暂停服务检查' % (item.get('service_name'), item.get('_id'))).set_type_project_service_check().set_par(item).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('pause service check success')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('pause service check exception:' + str(e))

    # 恢复服务检查
    def OAMP_resume_service_check(self, data):
        try:
            item = self._get_run_service_cehck_info(data=data)
            item['service_check_state_code_id'] = '1'  # 运行状态
            self._update_service_check_info(data=item)
            ApschedulerTaskFunc.getInstance(task_type= init.APS_TASKS.get('SERVICE_CHECK')).resume_apscheduler_task(data=data)

            msg = Msg.getInstance().set_msg('发布[%s]项目服务[%s]变更任务,恢复服务检查' % (item.get('service_name'), item.get('_id'))).set_type_project_service_check().set_par(item).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('resume service check success')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('resume service check exception:' + str(e))

    # 修改服务检查
    def OAMP_modify_service_check_info(self, data):
        try:
            service_check_rate = data.get('service_check_rate', 60)
            item = self._get_run_service_cehck_info(data=data)
            item['service_check_rate'] = service_check_rate
            _id = item.get('_id', None)
            r_re = R.setJson(key=item.get('_id'), value=item, ex=300)
            u_re = self._update_service_check_info(data=item)
            __sessionId__ = data.get('__sessionId__', 'sys')
            ApschedulerTaskFunc.getInstance(task_type= init.APS_TASKS.get('SERVICE_CHECK')).get_scheduler_ins().scheduler.reschedule_job(_id, trigger='interval', seconds=int(service_check_rate))
            if r_re is not None and u_re.getCode() == PR.Code_OK:
                msg = Msg.getInstance().set_msg('修改serviceCheck任务成功:[' + item.get('service_name') + ']').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(item).json()
            else:
                msg = Msg.getInstance().set_msg('修改serviceCheck任务失败:[' + item.get('service_name') + ']').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(item).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('修改服务检查信息成功')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '0'}).setMsg('修改服务检查信息异常:' + str(e))

    # 移除服务检查
    def OAMP_remove_service_check(self, data):
        try:
            ApschedulerTaskFunc.getInstance(task_type=init.APS_TASKS.get('SERVICE_CHECK')).remove_apscheduler_task(data=data)
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('remove service check success')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('remove service check exception:' + str(e))

    def OAMP_search_service_check_list(self, data):
        x = {
            'service_project_id': data.get('service_project_id', None)
        }
        return SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, par=data)

    # 运行服务检查
    def OAMP_run_service_check_task(self, data):
        try:
            x = {
                'service_project_id': data.get('service_project_id', None),
                'id': data.get('_id', None)
            }
            count_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, only=['id'], par={'pageSize': 1})
            count = count_res.getPageCount()
            if count > 0:
                page_size = 20
                threads = []
                for i in range(1, int(count / page_size + 2)):
                    service_check_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, par={'pageSize': page_size, 'pageNum': i})
                    if service_check_res.is_results_not_none():
                        for service_check_info in service_check_res.getData():
                            t = threading.Thread(target=self._check_post_service, args=(service_check_info, True,))
                            t.start()
                            threads.append(t)
                for t in threads:
                    t.join()
            return PR.getInstance().setCode(PR.Code_OK).setResult({'success': '1'}).setMsg('运行服务检查成功')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'success': '0'}).setMsg('运行服务检查异常:' + str(e))

    # 更新service_check 信息
    def _update_service_check_info(self, data):
        R.setJson(key=data.get('_id'), value=data, ex=300)
        # 修改aps的状态
        return SingleTableOpt.getInstance().setBO(ServiceCheckBo).setData(data=data).update()

    # 获取项目服务检查信息
    def get_project_service_check_info(self, service_project_id):
        try:
            res = []
            x = {'service_project_id': service_project_id}
            count_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, only=['id'], par={'pageSize': 1})
            count = count_res.getPageCount()
            if count > 0:
                page_size = 20
                for i in range(1, int(count / page_size + 2)):
                    service_check_res = SingleTableOpt.getInstance().setBO(ServiceCheckBo).search(filters=x, par={'pageSize': page_size, 'pageNum': i})
                    if service_check_res.is_results_not_none():
                        for r in service_check_res.getData():
                            res.append(r)
            return PR.getInstance().setCode(PR.Code_OK).setResult({}).setData(res).setMsg('获取项目服务信息成功')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({}).setMsg('获取项目服务信息异常:' + str(e))


def getInstance():
    return ServiceCheckTask()
