#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import datetime, threading, time
from os import path
import os
from bin.logic.func.upload import CDN
from bin import init
from bin.base.data import Path
from bin.base.sys import PR
from bin.base.sys import Msg
from bin.init import RunTimeState
from bin.logic.BO.OAMP.ToolBo import ToolBo
from bin.base.sys import SingleTableOpt
from bin.base.tool import RabbitMQ
from bin.base.data import Data
from bin.logic.BO.OAMP.UploadBo import UploadBo
from bin.logic.func.setting import CodeSetting
from bin.base.log import Logger

L = Logger.getInstance('upload.log')


class CDNUpload(object):
    def __init__(self):
        pass

    # 转移CDN状态 # 0 转移等待 1 转移中 2 转移成功 3 转移失败

    # 解决方案
    # 设置一个全局线程状态，判定是否中行完毕，同时控制上传线程数量
    # 启动一个线程去执行上传任务
    # 再启动一个线程去计时器

    def MQ_start(self, msg_data):
        L.debug('MQ_start :%s' % str(msg_data))
        # 更改上传状态 为开始上传
        start = datetime.datetime.now()  # 记录开始时间
        # 给线程一个随机ID
        thread_id = Data.getUUID()
        RunTimeState.UPLOAD_THREAD_info.__setitem__(thread_id, thread_id)
        t_timer = threading.Thread(target=self.upload_timer, name='upload_timer', args=(msg_data, start, thread_id))  # 开启线程，执行上传操作
        t_upload = threading.Thread(target=self.upload_to_cdn, name='upload_to_cdn', args=(msg_data, start, thread_id))  # 开启线程，执行上传操作
        t_timer.start()  # 又启动了一个孤儿线程
        t_upload.start()  # 启动了一个孤儿线程

    def upload_timer(self, msg_data, start, thread_id):
        data = Data.str_to_json(msg_data.get('par'))
        while True:
            if RunTimeState.UPLOAD_THREAD_info.get(thread_id) == thread_id:
                current = datetime.datetime.now()  # 记录当前时间
                # 更改上传状态 为上传中
                data['to_cdn_state_code_id'] = '1'  # 上传中
                data['toCdnConsumedTime'] = str((current - start).total_seconds())
                SingleTableOpt.getInstance().setBO(UploadBo).setData(data).update()
                time.sleep(RunTimeState.UPLOAD_THREAD_SLEEP_TIME)  # 先休息5s
            else:
                # 线程已经被清理掉了，已经计时完毕
                break

    # 转移到cdn 功能
    def upload_to_cdn(self, msg_data, start, thread_id):
        try:
            L.debug('upload_to_cdn: %s' % str(msg_data))
            data = Data.str_to_json(msg_data.get('par'))
            project = data.get('upload_project_id')
            x = {
                'tool_project_id': project
            }
            res_cnd_info = SingleTableOpt.getInstance().setBO(ToolBo).search(filters=x)
            L.debug('res_cnd_info: %s' % str(res_cnd_info.getData()))
            cnd_info = res_cnd_info.getData()[0]
            file_path = data.get('filePath')
            file_name = data.get('fileName')
            file_size = int(str(data.get('fileSize')).split('KB')[0])
            cdn_ip = cnd_info.get('toolHost')
            cnd_port = cnd_info.get('toolPort')
            cnd_user = cnd_info.get('toolUser')
            cnd_password = cnd_info.get('toolPassword')
            cnd_root_path = data.get('cdnRootPath')

            remote_file = ''
            to_cdn_rule_code_id = data.get('to_cdn_rule_code_id', '0')
            if to_cdn_rule_code_id == '0' or to_cdn_rule_code_id == '':  # 默认规则
                remote_file = cnd_root_path + str(file_path).replace(init.ROOT_UPLOAD_PATH, '')
            elif to_cdn_rule_code_id == '4':  # 无规则
                remote_file = cnd_root_path + os.sep + file_name
            else:
                # 查询下上传cdn 目录规则
                par = {
                    'code': 'to_cdn_rule',
                    'codeId': to_cdn_rule_code_id,
                    'isCodeType': False
                }
                code_value_res = CodeSetting.getInstance().OAMP_getCodeValueInfo(data=par)
                if code_value_res.getCode() == PR.Code_OK and code_value_res.getData() is not None:
                    to_cdn_rule_code_value = code_value_res.getData().get('codeValue')
                    rule_path = Path.getInstance().getRulePath(rule=to_cdn_rule_code_value)
                    remote_file = cnd_root_path + rule_path + os.sep + file_name

            remote_dir = path.dirname(remote_file)
            ftp = CDN.getInstance(host=cdn_ip, port=cnd_port, username=cnd_user, password=cnd_password)
            if ftp.upLoadFile(localFile=file_path, remoteFile=remote_file, remoteDir=remote_dir):
                end = datetime.datetime.now()  # 记录上传结束时间
                data['to_cdn_state_code_id'] = '2'
                consume_time = (end - start).total_seconds()
                data['toCdnConsumedTime'] = str(consume_time)
                data['fileCdnPath'] = remote_file
                reliable_risk = int (file_size / consume_time)
                data['reliable_risk'] = reliable_risk
                if reliable_risk > 10000:
                    data['reliability_state_code_id'] = '50'
                elif reliable_risk > 4000:
                    data['reliability_state_code_id'] = '70'
                elif reliable_risk > 2500:
                    data['reliability_state_code_id'] = '80'
                elif reliable_risk > 2000:
                    data['reliability_state_code_id'] = '90'
                else:
                    data['reliability_state_code_id'] = '100'
                SingleTableOpt.getInstance().setBO(UploadBo).setData(data).update()
                # 向 MQ 中发送消息
                msg_str = 'CDN转移文件,[%s]到[%s],转移成功，耗时%ss' % (file_path, remote_file, (end - start).total_seconds())
                user_name = msg_data.get('user_name')
                msg = Msg.getInstance().set_msg(msg_str).set_user_name(user_name).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                # 修改数据库
            else:
                data['to_cdn_state_code_id'] = '3'
                data['toCdnConsumedTime'] = '0'
                SingleTableOpt.getInstance().setBO(UploadBo).setData(data).update()
                msg_str = 'CDN转移文件,[%s]到[%s],转移失败' % (file_path, remote_file)
                msg = Msg.getInstance().set_msg(msg_str).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            del RunTimeState.UPLOAD_THREAD_info[thread_id]
        except Exception as e:
            L.exception('upload_to_cdn exception:%s' % str(e))


def getInstance():
    return CDNUpload()
