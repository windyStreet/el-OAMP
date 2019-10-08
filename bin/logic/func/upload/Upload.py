#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin import init
from bin.base.sys import SingleTableOpt, Msg, PR
from bin.base.sys.Session import SessionDataOpt
from bin.base.tool import RabbitMQ
from bin.base.log import Logger
from bin.logic.BO.OAMP.UploadBo import UploadBo

L = Logger.getInstance()


class Upload(object):
    def __init__(self):
        pass

    def OAMP_search_upload_list(self, data):
        x = {
            'upload_project_id': data.get('upload_project_id', ''),
            'fileName__contains': data.get('fileName', ''),
            'to_cdn_state_code_id': data.get('to_cdn_state_code_id', ''),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(UploadBo).search(filters=x, par=data)

    # 重新启动转移至cdn任务
    def OAMP_retransmission(self, data):
        L.debug('OAMP_retransmission ： %s' % str(data))
        session_id = data.get('__sessionId__')
        _PR = PR.getInstance()
        file_name = data.get('fileName')
        if file_name is None:
            return _PR.setMsg('转移文件任务启动,调用参数错误').setCode(PR.Code_ERROR).setResult({'is_success': False})
        try:
            # 写入发布任务上传cnd消息
            user_name = SessionDataOpt(session_id).getUserName()
            msg = Msg.getInstance().set_msg('重新发布上传%s文件至CDN任务' % file_name).set_user_name(user_name).set_par(data).set_type_upload_to_cnd().json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return _PR.setMsg('转移文件任务启动成功').setCode(PR.Code_OK).setResult({'is_success': True})
        except Exception as e:
            L.error('转移文件%s，出现错误:%s' % (file_name, str(e)))
            return _PR.setMsg('转移文件任务启动失败').setCode(PR.Code_ERROR).setResult({'is_success': False})


def getInstance():
    return Upload()
