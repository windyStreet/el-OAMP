#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import threading
from bin import init
from bin.base.log import Logger
from bin.base.tool import RabbitMQ
from bin.base.data import Data
from bin.base.sys import Msg
from bin.logic.func.record import MailRecord

L = Logger.getInstance('sys.log')


class MailTask(object):
    def __init__(self):
        pass

    def runTask(self, ch, method, properties, body):
        try:
            info_str = str(body, encoding="utf-8")
            receive_item = {}
            if Data.check_json_format(info_str):
                receive_item = Data.str_to_json(str(body, encoding="utf-8"))
            else:
                L.error('%s has the error info : %s' % (init.MQ_QUEUE_MAIL, info_str))
            if receive_item.get('msg_type_code_id') == Msg.MSG_TYPE_EMAIL:
                user_name = receive_item.get('user_name', 'sys')
                send_msg = str(receive_item.get('msg')).replace('发布', '处理')
                msg = Msg.getInstance().set_msg(send_msg).set_user_name(user_name).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

                MailRecord.getInstance().MQ_start(msg_data=receive_item)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                L.error('%s has the error type data : %s' % (init.MQ_QUEUE_UPLOAD, receive_item))
                msg = Msg.getInstance().set_msg('邮件发送任务队列中出现异常类型数据:%s' % receive_item).set_par(receive_item).set_msg_level_error().json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送了异常消息，信息略过
        except Exception as e:
            L.exception('处理email任务时，邮件队列出现异常')
            msg = Msg.getInstance().set_msg('邮件队列处理异常').set_par(str(e)).set_msg_level_error().json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def exec(self):
        L.info('%s 开始运行' % threading.current_thread().name)
        # 默认空，走默认队列
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).receiveMsg(queue=init.MQ_QUEUE_MAIL, callback=self.runTask)

    def run(self):
        t = threading.Thread(target=self.exec, name='threadMailTask')
        t.start()


def getInstance():
    return MailTask()
