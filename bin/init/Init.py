#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import Logger
from bin.init import ConfInit
from bin.init import ClusterModeInit
from bin.init import TaskWorkInit
from bin.init import MemoryInit

L = Logger.getInstance()
'''
1、 配置文件
    1.1 配置文件初始化
    1.2 静态文件初始化
    1.3 集群模式初始化
    1.4 任务初始化
'''


class Init(object):
    def init(self):
        # 初始化本地配置到内存中
        L.info("1.1 init sys conf , starting ...")
        ConfInit.getInstance().init()
        L.info("1.1 init sys conf , starting ...")
        # 重新配置初始化ajax请求的http.js文件
        # http_js_init.rewrite_http_js()
        L.info("1.2 init memory data , starting ...")
        MemoryInit.getInstance().init()
        L.info("1.3 init cluster mode , starting ...")
        ClusterModeInit.getInstance().init()
        L.info("1.4 init system task , starting ...")
        TaskWorkInit.getInstance().init()
        ####################################################################################
        # 统计信息初始化
        # L.info("static data init")
        # 初始化统计项信息
        # L.info("init statistical_item , starting...")
        # Statistic_item_func.getInstance().init_exist_item()
        # 启动统计计算项任务
        # L.info("init compute data task , starting...")
        # Statistical_item_func.getInstance().start_compute()
        ####################################################################################
        # 日志接收初始化
        # L.info("log receive init")
        # L.info("init receive mongodb log , starting...")
        # MongoDB_log.getInstance().start()
