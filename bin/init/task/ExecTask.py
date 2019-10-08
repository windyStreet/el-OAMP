#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import threading
from bin import init
from bin.base.tool import RabbitMQ
from bin.base.data import Data
from bin.base.log import Logger
from bin.logic import MQ_logic

from bin.logic.func.common import PublishMQFunc

L = Logger.getInstance('sys.log')


class ExecTask(object):
    def __init__(self):
        self.MQ_ins = MQ_logic.getInstance()
        self.thread_exec_count = 1

    def exec(self):
        L.info('%s 开始运行' % threading.current_thread().name)
        try:
            if self.thread_exec_count > 3:
                L.error('%s 队列运行错误,尝试三次均失败,关闭该队列功能' % init.MQ_QUEUE_EXEC)
            else:
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS, ).receiveMsg(queue=init.MQ_QUEUE_EXEC, callback=self.runTask)
        except Exception as e:
            L.info('%s 队列运行异常:%s，重新启动' % (init.MQ_QUEUE_EXEC, str(e)))
            self.thread_exec_count += 1
            self.exec()

    def runTask(self, ch, method, properties, body):
        self.thread_exec_count = 1
        try:
            info_str = str(body, encoding="utf-8")
            if Data.check_json_format(info_str):
                receive_item = Data.str_to_json(info_str)
                project = receive_item.get('project')
                method_name = receive_item.get('method')
                par = Data.str_to_json(receive_item.get('par'))
                user_name = receive_item.get('user_name')
                exec_count = receive_item.get('exec_count', 4)
                try:
                    L.info('%s第%s次执行%s项目%s操作，参数为:%s' % (str(user_name), str(exec_count), str(project), str(method_name), str(par)))
                    if not getattr(self.MQ_ins, method_name)(par):
                        PublishMQFunc.getInstance().set_project(project).set_method(method_name).set_par(par).set_user_name(user_name).add_exec_count(exec_count).publish()
                except Exception as e:
                    L.exception('%s项目执行%s功能队列异常:%s，重新放置任务' % (str(project), str(method), str(e)))
                    PublishMQFunc.getInstance().set_project(project).set_method(method_name).set_par(par).set_user_name(user_name).add_exec_count(exec_count).publish()
            else:
                L.error('执行功能队列传递参数错误:%s' % (str(info_str)))
        except Exception as e:
            L.error('执行功能队列异常:%s' % (str(e)))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        t = threading.Thread(target=self.exec, name='threadExecTask')
        t.start()


def getInstance():
    return ExecTask()
