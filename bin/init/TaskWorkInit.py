#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import Logger
from bin.base.tool import JsonFileFunc
from bin.base.data import Path
from bin.init.task import UploadTasK
from bin.init.task import MsgRecordTask
from bin.init.task import MailTasK
from bin.init.task import ExecTask
from bin.init.task import ProjectServiceCheckTask
from multiprocessing import Pool

L = Logger.getInstance('sys.log')
J = JsonFileFunc.getInstance()
P = Path.getInstance()


# 启动任务初始化
class TaskWorkInit(object):
    def __init__(self):
        pass

    def init(self):
        L.info('start process to exec sys task')
        p = Pool()
        p.apply_async(func=MsgRecordTask.getInstance().run(), args=())  # 消息记录任务
        p.apply_async(func=ExecTask.getInstance().run(), args=())  # 执行任务
        p.apply_async(func=ProjectServiceCheckTask.getInstance().run(), args=())  # 项目服务检查任务
        p.apply_async(func=UploadTasK.getInstance().run(), args=())  # 上传任务
        p.apply_async(func=MailTasK.getInstance().run(), args=())  # 邮件任务
        p.close()
        p.join()
        # p = Process(target= ExecTask.getinstance().run(), args=())
        # p.start()
        # p.join()


def getInstance():
    return TaskWorkInit()
