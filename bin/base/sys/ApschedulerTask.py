#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import *
from bin import init
from bin.base.data import Path
from bin.base.log import Logger
from apscheduler.schedulers.tornado import TornadoScheduler

P = Path.getInstance()
L = Logger.getInstance('ApschedulerTask.log')


# logging.basicConfig(level=logging.INFO,
#                     format=L.formatter,
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename=L.log_path,
#                     filemode='a', )

class ApschedulerTask(object):
    def __init__(self, task_type):
        if task_type not in init.SCHEDULERS.keys(): # MongoDB 参数
            host = init.CONF_INFO.get(init.CONTEXT + 'mongodb').get('toolHost')
            port = init.CONF_INFO.get(init.CONTEXT + 'mongodb').get('toolPort')
            database = init.CONF_INFO.get(init.CONTEXT + 'mongodb').get('toolName')
            collection = task_type
            client = MongoClient(host, port)
            jobstores = {
                'mongo': MongoDBJobStore(collection=collection, database=database, client=client),
                'default': MemoryJobStore()
            }
            executors = {
                'default': ThreadPoolExecutor(10),
                'processpool': ProcessPoolExecutor(3)
            }
            job_defaults = {
                'coalesce': False,
                'max_instances': 3,
                'misfire_grace_time': 60
            }
            self.jobstore = 'mongo'
            self.scheduler = TornadoScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)  # self.scheduler = BlockingScheduler()
            init.SCHEDULERS.update({task_type: self.scheduler})
        else:
            self.scheduler = init.SCHEDULERS.get(task_type)

    # 获取任务列表
    def get_task_list(self):
        return self.scheduler.get_jobs()

    # 获取指定任务
    def get_task(self, job_id):
        if job_id is None:
            return []
        return self.scheduler.get_job(job_id=job_id, jobstore=self.jobstore)

    # 移除指定作业
    def remove_task(self, job_id):
        return self.scheduler.remove_job(job_id=job_id)

    # 移除全部作业
    def remove_all_task(self):
        return self.scheduler.remove_job()

    # 暂停指定作业
    def pause_task(self, job_id):
        self.scheduler.pause_job(job_id)

    # 暂停全部作业
    def pause_all_task(self):
        self.scheduler.pause_job()

    # 恢复指定作业
    def resume_task(self, job_id):
        self.scheduler.resume_job(job_id=job_id)

    # 恢复所有作业
    def resume_all_task(self):
        self.scheduler.resume_job()

    # 关闭scheduler
    def shut_down(self):
        return self.scheduler.shutdown()

    # 添加任务，暂时依据源文件方式处理
    def __add_task(self):
        pass

    def my_listener(self, event):
        if hasattr(event, 'exception') and event.exception:
            L.exception(event.job_id + '任务出错了！！！！！！,exception:' + str(event.exception))

    def start_task(self):
        self.scheduler.add_listener(self.my_listener, EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN | EVENT_SCHEDULER_PAUSED |
                                    EVENT_SCHEDULER_RESUMED | EVENT_EXECUTOR_ADDED | EVENT_EXECUTOR_REMOVED |
                                    EVENT_JOBSTORE_ADDED | EVENT_JOBSTORE_REMOVED | EVENT_ALL_JOBS_REMOVED |
                                    EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_MODIFIED | EVENT_JOB_EXECUTED |
                                    EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_SUBMITTED | EVENT_JOB_MAX_INSTANCES)
        # self.scheduler._logger = L.logging
        try:
            self.scheduler.start()
        except Exception as e:
            L.exception('scheduler start exception:' + str(e))


def getInstance(task_type='apscheduler_task_bo'):
    return ApschedulerTask(task_type=task_type)
