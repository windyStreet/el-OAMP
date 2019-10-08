#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import threading, json
from bin import init
from bin.base.sys import Msg
from bin.base.tool import RabbitMQ
from bin.base.data import Data
from bin.base.log import Logger
from bin.logic.func.record import MsgRecord

L = Logger.getInstance('sys.log')


class MsgRecordTask(object):
    def __init__(self):
        pass

    def runTask(self, ch, method, properties, body):
        info_str = str(body, encoding="utf-8")
        if Data.check_json_format(info_str):
            receive_item = json.loads(str(body, encoding="utf-8"))
            # 流水消息记录处理
            MsgRecord.getInstance().record(data=receive_item)
            if receive_item.get('msg_type_code_id') == Msg.MSG_TYPE_UPLOAD_TO_CDN: # 上传
                # 上传任务将消息转发到上传队列
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_UPLOAD, msg=receive_item)
            elif receive_item.get('msg_type_code_id') == Msg.MSG_TYPE_PROJECT_SERVICE_CHECK: # 服务检查
                # 项目服务变更任务将消息转发到项目服务变更队列
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_PROJECT_SERVICE, msg=receive_item)
            elif receive_item.get('msg_type_code_id') == Msg.MSG_TYPE_EMAIL: # 邮件
                # 邮件任务消息转发到邮件队列
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MAIL, msg=receive_item)
            else:
                pass
                # 判断消息类型，处理消息内容
        else:
            L.error('%s has the error info : %s' % (init.MQ_QUEUE_UPLOAD, info_str))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def exec(self):
        L.info('%s 开始运行' % threading.current_thread().name)
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS, ).receiveMsg(queue=init.MQ_QUEUE_MSG, callback=self.runTask)

    def run(self):
        t = threading.Thread(target=self.exec, name='threadMsgRecordTask')
        t.start()


def getInstance():
    return MsgRecordTask()
