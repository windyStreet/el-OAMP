from bin.base.sys import PR
from bin.logic import Inner_logic
from bin.base.data import PostUntil
from bin.base.sys import Msg
from bin.base.data import Time
from bin.base.tool import RabbitMQ
from bin import init
from bin.logic.func.task import ApschedulerTaskFunc
from bin.base.log import Logger

L = Logger.getInstance()


class ProjectOptResultCheck(object):
    def __init__(self):
        pass

    # 启动服务检查
    def start_opt_result_check(self, user_name, ips, opt_id, project_name, service_name, service_url):
        ins = ApschedulerTaskFunc.getInstance(init.APS_TASKS.get('PROJECT_OPT')).get_scheduler_ins()
        ins.scheduler.add_job(self.run_opt_result_check, args=[ips, project_name, opt_id, service_url, user_name], id=opt_id, trigger='interval', seconds=3, replace_existing=True, jobstore='mongo')
        msg = Msg.getInstance().set_msg('添加%s项目%s操作检查任务[%s]' % (project_name, service_name,opt_id)).set_user_name(user_name=user_name).set_type_sys_log().json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return True

    # 运行操作结果检查
    def run_opt_result_check(self, ips, project_name, opt_id, service_url, user_name):
        # 开始请求远程服务然后进行处理
        po_ins = PostUntil.getInstance()
        for ip in ips:
            item = {
                'data': {
                    'method': 'getProjectStatus',
                    'projectName': project_name,
                    'opt_id': opt_id
                },
                'method': 'getProjectStatus'
            }
            url = service_url.replace('localhost', ip)
            par = {'url': url, 'json_par': item, 'time_out': 3, 'request_ip': ip}
            po_ins.add_thread(po_ins.pr_post, kwargs=par)
        po_ins.start().join()
        result = po_ins.res_queue.queue
        self.del_opt_result(queue_result=result, project_name=project_name, opt_id=opt_id, user_name=user_name)

    # 处理结果
    def del_opt_result(self, queue_result, project_name, opt_id, user_name):
        record_re = Inner_logic.getInstance().search_project_opt_record_info_by_id({'_id': opt_id})
        if record_re.is_result_not_none():
            record_data = record_re.getData()
            update_bean = self.get_cur_opt_update_info(queue_result=queue_result, record_data=record_data, opt_id=opt_id, user_name=user_name)
            u_re = Inner_logic.getInstance().update_project_opt_record_info(data=update_bean)
            if u_re.getCode() == PR.Code_OK:
                L.info('获取%s项目当前状态结果成功' % str(project_name))
            else:
                L.error('获取%s项目当前状态结果失败:%s' % (str(project_name), str(u_re.getMsg())))
        else:
            L.error('获取%s项目当前状态结果时，通过操作id【%s】未查询到操作记录' % (str(project_name), str(opt_id)))

    def get_cur_opt_update_info(self, queue_result, record_data, opt_id, user_name):
        record_data['remote_exec_count'] = record_data.get('remote_exec_count', 0) + 1
        count = len(queue_result)
        exec_finished_count = 0
        exec_success_count = 0
        remote_exec_result = []
        for re in queue_result:
            if re.is_result_not_none():
                remote_exec_result.append(re.getData())
                re_data = re.getData()
                is_finished = str(re_data.get('is_finished'))
                is_normal = str(re_data.get('is_normal'))
                if is_finished == '1':
                    exec_finished_count += 1
                    if is_normal == '1':
                        exec_success_count += 1
                else:
                    break
            else:
                # 返回值失败的接口
                L.error('处理项目操作结果时,返回结果PR无法正常解析%s' % str(re))
        record_data['remote_exec_result'] = remote_exec_result
        if count > 0 and count == exec_finished_count:
            exec_state_code_id = '2'  # 所有服务器完成操作
            record_data['exec_state_code_id'] = exec_state_code_id
            record_data['project_opt_end_time'] = Time.get_update_time()
            if count == exec_success_count:
                is_opt_success = '1'  # 所有服务器成功完成操作
                if record_data.get('project_opt_type_code_id') in ('3', '4', '5', '6'):  # 3资源替换、4标记更新、5全量更新、6增量更新
                    record_data['is_able_rollback'] = '1'
            else:
                is_opt_success = '0'
            self.__update_project_info(record_data, is_opt_success)
            ApschedulerTaskFunc.getInstance(task_type=init.APS_TASKS.get('PROJECT_OPT')).remove_apscheduler_task(data={'_id': opt_id, 'user_name': user_name})  # 清理掉获取项目执行状态的定时任务
            record_data['is_opt_success'] = is_opt_success
        return record_data

    def __update_project_info(self, record_data, is_opt_success):
        project_opt_version = record_data.get('project_opt_version')
        project_opt_last_version = record_data.get('project_opt_last_version')
        project_id = record_data.get('project_id')
        project_re = Inner_logic.getInstance().search_project_info_by_id({'project_id': project_id})
        if project_re.is_result_not_none():
            project_data = project_re.getData()
            if is_opt_success == '1':
                project_data['project_state_code_id'] = 'RUNNING'  # 运行中
            else:
                project_data['project_state_code_id'] = 'EXCEPTION'  # 异常中
            project_data['project_version'] = project_opt_version
            project_data['project_last_version'] = project_opt_last_version
            u_re = Inner_logic.getInstance().update_project_info(data=project_data)  # 更新项目信息为正常中 | 异常中
            if u_re.is_result_not_none():
                L.info('服务检查返回，修改项目状态成功')
            else:
                L.error('服务检查返回，修改项目状态失败')
        else:
            L.error('服务检查返回，修改项目状态信息时，未查询到项目信息')


def getInstance():
    return ProjectOptResultCheck()
