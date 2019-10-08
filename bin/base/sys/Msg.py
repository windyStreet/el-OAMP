#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.data import Time
from bin import init
from bin.base.sys.Session import SessionDataOpt

#  消息类型
MSG_TYPE_INTERFACE = 'interface'  # 接口记录
MSG_TYPE_UPLOAD_TO_CDN = 'upload_to_cdn'  # 上传CDN
MSG_TYPE_PROJECT_SERVICE_CHECK = 'project_service_check'  # 项目服务检查
MSG_TYPE_PROJECT_RES_UPLOAD = 'project_res_upload'  # 项目资源上传
MSG_TYPE_PROJECT_UPDATE = 'project_update'  # 项目更新
MSG_TYPE_PROJECT_FULL_UPDATE = 'project_full_update'  # 项目全量更新
MSG_TYPE_PROJECT_INC_UPDATE = 'project_inc_update'  # 项目增量更新
MSG_TYPE_PROJECT_ROLLBACK = 'project_rollback'  # 项目回滚
MSG_TYPE_PROJECT_RESTART = 'project_restart'  # 项目重启
MSG_TYPE_SYS_LOG = 'sys_log'  # 系统日志
MSG_TYPE_EXEC_LOG = 'exec_log'  # 执行日志
MSG_TYPE_FLOW_LOG = 'flow_log'  # 流水日志
MSG_TYPE_EMAIL = 'e-mail'  # 流水日志

# 消息等级
MSG_LEVEL_INFO = 'info'  # 一般的
MSG_LEVEL_EXCEPTION = 'exception'  # 异常的
MSG_LEVEL_ERROR = 'error'  # 错误的
MSG_LEVEL_FATAL = 'fatal'  # 致命的


class Msg(object):
    def __init__(self):
        self.msg = '系统日志'
        self.user_name = 'sys'
        self.send_time = Time.get_create_time()
        self.source = init.CONTEXT
        self.par = None
        self.msg_level_code_id = MSG_LEVEL_INFO  # 默认info等级
        self.msg_type_code_id = MSG_TYPE_FLOW_LOG  # 默认流水日志

    def json(self):
        """JSON format data."""
        json = {
            'msg': self.msg,
            'user_name': self.user_name,
            'send_time': self.send_time,
            'source': self.source,
            'par': self.par,
            'msg_level_code_id': self.msg_level_code_id,
            'msg_type_code_id': self.msg_type_code_id
        }
        return json

    def set_msg(self, msg=None):
        self.msg = msg
        return self

    def set_user_name(self, user_name=None, session_id=None):
        if user_name is not None:
            self.user_name = user_name
            return self
        if session_id is not None:
            self.user_name = SessionDataOpt(sessionId=session_id).getUserName()
        return self

    def set_source(self, source):
        self.source = source
        return self

    def set_par(self, par=None):
        self.par = par
        return self

    def set_msg_level(self, msg_level=None):
        self.msg_level_code_id = msg_level
        return self

    def set_msg_level_info(self):
        self.msg_level_code_id = MSG_LEVEL_INFO
        return self

    def set_msg_level_exception(self):
        self.msg_level_code_id = MSG_LEVEL_EXCEPTION
        return self

    def set_msg_level_error(self):
        self.msg_level_code_id = MSG_LEVEL_ERROR
        return self

    def set_msg_level_fatal(self):
        self.msg_level_code_id = MSG_LEVEL_FATAL
        return self

    def set_msg_type(self, msg_type=None):
        self.msg_type_code_id = msg_type
        return self

    # 设置消息类型为:上传队列
    def set_type_upload_to_cnd(self):
        self.msg_type_code_id = MSG_TYPE_UPLOAD_TO_CDN
        return self

    # 设置消息类型为:项目服务检查
    def set_type_project_service_check(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_SERVICE_CHECK
        return self

    # 设置消息类型为:项目文件上传
    def set_type_project_res_upload(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_RES_UPLOAD
        return self

    # 设置消息类型为:项目更新
    def set_type_project_update(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_UPDATE
        return self
    # 设置消息类型为:项目全量更新
    def set_type_project_full_update(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_FULL_UPDATE
        return self
    # 设置消息类型为:项目增量更新
    def set_type_project_inc_update(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_INC_UPDATE
        return self

    # 设置消息类型为:项目回滚
    def set_type_project_rollback(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_ROLLBACK
        return self
    # 设置消息类型为:项目重启
    def set_type_project_restart(self):
        self.msg_type_code_id = MSG_TYPE_PROJECT_RESTART
        return self

    # 邮件类型任务
    def set_type_mail(self):
        self.msg_type_code_id = MSG_TYPE_EMAIL
        return self

    # 流水类型消息
    def set_type_flow_log(self):
        self.msg_type_code_id = MSG_TYPE_FLOW_LOG
        return self

    # 系统类型消息
    def set_type_sys_log(self):
        self.msg_type_code_id = MSG_TYPE_SYS_LOG
        return self

    # 接口类型消息
    def set_type_interface(self):
        self.msg_type_code_id = MSG_TYPE_INTERFACE
        return self


def getInstance():
    return Msg()
