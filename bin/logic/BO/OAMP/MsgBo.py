# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(rpip install pipreqs
# equired=True, max_length=100)
#     fatherCode = StringField(max_length=100)


class MsgBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField() # 消息处理时间
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    msg = StringField()  # 消息内容
    user_name = StringField(default='sys')  # 消息操作人
    send_time = StringField()  # 消息发生时间
    source = StringField()  # 消息来源
    par = StringField()  # 消息发生位置的调用参数
    msg_level_code_id = StringField()  # 消息严重等级
    msg_type_code_id = StringField()  # 消息类型

    # 系统日志等级 __init__
    # MSG_LEVEL_INFO = 'sys_info'  # 一般的
    # MSG_LEVEL_ERROR = 'sys_error'  # 错误的
    # MSG_LEVEL_EXCEPTION = 'sys_exception'  # 异常的
    # MSG_LEVEL_FATAL = 'sys_fatal'  # 致命的

    # 消息类型
    # MSG_TYPE_EXEC_LOG = 'exec_log'  # 执行日志
    # MSG_TYPE_SYS_LOG = 'sys_log'  # 系统日志
    # MSG_TYPE_FLOW_LOG = 'flow_log'  # 流水日志
    # MSG_TYPE_UPLOAD_TASK = 'flow_log'  # 流水日志
