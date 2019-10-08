#!/usr/bin/env python
# !-*- coding:utf-8 -*-

# auth WindyStreet 2017-11-29
import sys

""""项目主文件"""
# 初始化项目路径
sys.path.append(sys.path[0].replace("/bin", ""))

import tornado.web
from bin.service import Service
from bin.service import SocketService
from bin.logic.func.message import Chat
from bin.service import Html_service
from tornado.options import define, options
from bin.init import Init
from bin.base.data import FileUntil, Path
from bin.base.log import Logger
from bin import init
import os
from bin.base.sys import ApschedulerTask


P = Path.getInstance()
L = Logger.getInstance()

if __name__ == "__main__":
    L.info("############################################################################")
    L.info("初始化参数")  # 初始化参数
    Init.Init().init()
    L.info("############################################################################")
    L.info("初始化应用")
    port = init.PORT
    context = init.CONTEXT
    define("port", default=port, help="run on the given port", type=int)
    tornado.options.options.logging = "error"  # 定义系统默认日志等级
    tornado.options.parse_command_line()

    L.info("############################################################################")
    L.info("init 3 , auto create the router")
    html_files = FileUntil.getInstance().get_html_file_relation_path(dir_path=P.webPath)
    handlers = [(r"/" + context + "/service", Service.Service),
                (r"/" + context + "/socketService", SocketService.MessageWSHandler),  # socket
                (r"/" + context + "/chat", Chat.ChatHandler),  # chat
                (r"/" + context + "/uploadFile", Service.uploadFile),  # 上传文件接口
                (r"/" + context + "/Open_falcon_query", Service.Open_falcon_query)  # open-falcon 接口
                ]
    handlers.append(('.*', Html_service.html))
    # 静态文件路径设置
    setting = dict(
        static_path=P.webPath + os.sep + 'static',
        autoreload=False,
        debug=False,
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        # xsrf_cookies=True
    )
    # 应用设置
    app = tornado.web.Application(
        handlers=handlers,
        **setting
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    L.info("############################################################################")
    # 检测主控服务问题 fixed @me 2018年1月23日22:47:12
    for k, v in init.APS_TASKS.items():
        ApschedulerTask.getInstance(task_type=v).start_task()  # 需保证只有一个实例在运行
        L.info('启动定时任务:%s' % str(v))
    L.debug("step4 , start web server")
    L.info("web server started , port is : %s , context is : %s ", port, context)
    tornado.ioloop.IOLoop.instance().start()
    # from tornado.ioloop import IOLoop
    # IOLoop.current().run_sync()
