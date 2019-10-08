# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.sys import Msg
from bin.base.tool import RabbitMQ
from bin.base.sys import PR
from bin.base.sys import ApschedulerTask


class ApschedulerTaskFunc(object):
    def __init__(self, task_type):
        self.task_type = task_type

    # 暂停任务 serviceCheckBo
    def pause_apscheduler_task(self, data):
        __sessionId__ = data.get('__sessionId__')
        job_id = data.get('_id', None)
        if job_id is not None:
            ApschedulerTask.getInstance(self.task_type).pause_task(job_id=job_id)
            msg = Msg.getInstance().set_msg('暂停任务[%s]' % job_id).set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
        else:
            ApschedulerTask.getInstance(self.task_type).pause_all_task()
            msg = Msg.getInstance().set_msg('暂停全部任务').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

    # 恢复任务 serviceCheckBo
    def resume_apscheduler_task(self, data):
        __sessionId__ = data.get('__sessionId__')
        job_id = data.get('_id', None)
        if job_id is not None:
            ApschedulerTask.getInstance(self.task_type).resume_task(job_id=job_id)
            msg = Msg.getInstance().set_msg('恢复任务[%s]' % job_id).set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
        else:
            ApschedulerTask.getInstance(self.task_type).resume_all_task()
            msg = Msg.getInstance().set_msg('恢复全部任务').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

    # 移除任务
    def remove_apscheduler_task(self, data):
        __sessionId__ = data.get('__sessionId__')
        user_name = data.get('user_name')
        job_id = data.get('_id', None)
        if job_id is not None:
            ApschedulerTask.getInstance(self.task_type).remove_task(job_id=job_id)
            msg = Msg.getInstance().set_msg('移除任务[%s]' % job_id).set_user_name(session_id=__sessionId__, user_name=user_name).set_type_sys_log().set_par(data).json()
        else:
            ApschedulerTask.getInstance(self.task_type).resume_all_task()
            msg = Msg.getInstance().set_msg('移除全部任务').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

    # 获取任务操作实例
    def get_scheduler_ins(self):
        return ApschedulerTask.getInstance(self.task_type)


def getInstance(task_type=None):
    return ApschedulerTaskFunc(task_type=task_type)
