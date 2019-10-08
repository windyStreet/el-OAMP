#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.data import Data
from bin.base.sys import Msg
from bin.base.sys import PR
from bin.logic.func.record import Falcon_mail_data
from email.mime.text import MIMEText
from bin.base.tool import Mail
from bin.base.tool import RabbitMQ
from bin.base.log import Logger

L = Logger.getInstance()


class MailRecord(object):
    def __init__(self):
        pass

    def mail_falcon(self, data):
        # 先处理数据， 将邮件内容、 人拆分成多条消息
        # 分条发送邮件
        receivers, header, content, = Falcon_mail_data.getInstance(data).deal_data()

        for receiver in receivers:
            par_data = {
                'sender_account': None,
                'receivers': receiver,
                'msg': {
                    'content': content,
                    'subject': header
                },
                'type': 'open-falcon'
            }
            msg = Msg.getInstance().set_msg('发布 open-falcon 给 %s 发送预警的邮件任务' % receiver).set_par(par_data).set_user_name(user_name='open-falcon').set_type_mail().json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return PR.getInstance().setResult({"is_success": True}).setCode(PR.Code_OK).setMsg('open-falcon 发送邮件任务已经递出')

    # 消息队列发送邮件
    def MQ_start(self, msg_data):
        data = Data.str_to_json(msg_data.get('par'))
        if data.get('type') == 'open-falcon':
            sender_account = data.get('sender_account')
            receivers = data.get('receivers')
            msg = data.get('msg')
            content = msg.get('content')
            subject = msg.get('subject')
            mail_msg = MIMEText(content, 'html', 'utf-8')
            mail_msg['Subject'] = subject

            return Mail.getInstance(init.ROOT_MAIL_DS).send_mail(sender_account=sender_account, receiver_accounts=receivers, msg=mail_msg)

        else:
            L.info('发送普通邮件')


def getInstance():
    return MailRecord()
