#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
from bin import init
from bin.base.sys import SingleTableOpt, PR, Msg
from bin.base.sys.Session import SessionDataOpt
from bin.base.log import Logger
from bin.base.data import Data, Path, Time
from bin.logic.BO.OAMP.UploadBo import UploadBo
from bin.base.tool import RabbitMQ, Redis

P = Path.getInstance()
L = Logger.getInstance()
R = Redis.getInstance(ds=init.ROOT_REDIS_DS, db=init.FILE_UPLOAD_REDIS_DB)


class FileOpt(object):
    def __init__(self, data):
        self.__sessionId__ = data.get('__sessionId__')
        self.isToCdn = True if data.get('isToCdn', None) is not None and data.get('isToCdn', None) == 'true' else False  # 是否转移到cdn中
        self.upload_project_id = data.get('upload_project_id', None)  # 上传项目id
        self.cdnRootPath = data.get('cdnRootPath', None)  # cdn根路径
        self.to_cdn_rule_code_id = data.get('to_cdn_rule_code_id', 0)  # 转移cdn目录规则
        self.upload_mode_code_id = data.get('upload_mode_code_id', '1')  # 通用 1 、强制2 、覆盖 3

        self.rootPath = init.ROOT_UPLOAD_PATH
        self.chunkNumber = data.get('chunkNumber', None)
        self.chunkSize = data.get('chunkSize', None)
        self.currentChunkSize = data.get('currentChunkSize', None)
        self.fileSize = str(int(int(data.get('totalSize', 0)) / 1024) + 1) + 'KB'
        self.identifier = data.get('identifier', None)
        self.fileName = data.get('filename', None)
        self.relativePath = data.get('relativePath', None)
        self.totalChunks = data.get('totalChunks', None)
        self.cdnPath = data.get('cdnPath', None)
        self.content = data.get('content', None)
        self.currentFilename = self.fileName
        self.filePath = self.rootPath + Time.getYMDpath() + os.sep + self.currentFilename
        self.tempDir = self.rootPath + Time.getYMDpath() + os.sep + self.identifier
        self.tempFileName = self.identifier + self.chunkNumber + ".temp"
        self.tempFilePath = self.tempDir + os.sep + self.tempFileName

        self.fileCdnPath = None
        self.upload_state_code_id = 'waiting'  # 未开始上传
        self.isToCdnSuccess = False
        self.downLoadCount = 0
        self.cdnDownLoadCount = 0
        self.insertData = None

    def __search_upload_info(self):
        # 判断同一个文件的依据 同一个项目 同一个文件名称
        x = {
            'upload_project_id': self.upload_project_id,
            'fileName': self.fileName,
        }
        data = {
            'order': '-createTime'
        }
        return SingleTableOpt.getInstance().setBO(UploadBo).search(filters=x, par=data)

    # 插入上传信息
    def __insert_upload_info(self):
        return SingleTableOpt.getInstance().setBO(UploadBo).setData(Data.classToDict(self)).insert()

    # 检查文件所有分片是否上传完成
    def chekIsSuccess(self):
        for chunk in range(1, int(self.totalChunks) + 1):
            if not os.path.exists(self.tempDir + os.sep + self.identifier + str(chunk) + ".temp"):
                return False
        return True

    # 文件分片临时文件保存
    def createWriteTempFile(self):
        # 记录文档
        try:
            # 检查保存保存临时文件的文件夹是否存在，不存在则创建
            if not os.path.exists(self.tempDir):
                os.makedirs(self.tempDir)
            # 创建临时缓存文件
            with open(self.tempFilePath, "wb") as tmpFile:
                tmpFile.write(self.content)
            return True
        except Exception as e:
            L.info("create %s failed %s" % (str(self.tempFilePath), str(e)))
            return False

    # 合并临时文件
    def mergeTempFile(self):
        try:
            with open(self.filePath, 'wb') as target_file:  # 创建新文件
                for chunk in range(1, int(self.totalChunks) + 1):
                    temp = self.tempDir + os.sep + self.identifier + str(chunk) + ".temp"
                    source_file = open(temp, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
            return True
        except IOError as e:
            L.exception("Merge temporary file exception : %s", e)
            return False

    # 删除临时文件
    def delTempFile(self):
        try:
            for chunk in range(1, int(self.totalChunks) + 1):
                temp = self.tempDir + os.sep + self.identifier + str(chunk) + ".temp"
                os.remove(temp)  # 删除该分片，节约空间
            os.removedirs(self.tempDir)
            return True
        except IOError as e:
            L.exception("delete temporary file exception : %s", e)
            return False

    # 文件上传
    def OAMP_uploadFile(self, data):
        # 通用 1 、强制2 、覆盖 3
        # 添加防重策略
        if self.upload_mode_code_id == '1':  # 通用上传 重复文件不允许上传
            return self.upload_file_only(data)
        if self.upload_mode_code_id == '2':  # 强制上传 重复文件也可以上传
            return self.upload_file_force(data)
        if self.upload_mode_code_id == '3':  # 覆盖上传 覆盖原路径上传[保持源文件路径不变]
            return self.upload_file_over(data)

    #  防重复策略都需要做 ，防止一个文件上传多次
    def upload_file_only(self, data):  # 防重复上传策略
        # 先来查询下数据库
        _PR = PR.getInstance()
        if self.__search_upload_info().is_results_not_none():
            return _PR.setResult({'isUpload': False}).setCode(PR.Code_WARNING).setMsg('%s文件已存在' % self.fileName)
        # 没有相同的，就有上传一个就行了
        return self.upload_file_force(data)

    # 强制覆盖
    def upload_file_over(self, data):
        _db_upload_info = self.__search_upload_info()
        if _db_upload_info.is_results_not_none() and _db_upload_info.getData() is not None:
            _db_upload_data = _db_upload_info.getData()[0] # 选取最新一次的文件覆盖
            self.filePath = _db_upload_data.get('filePath')  # 强制文件回归到之前的上传路径上
        return self.upload_file_force(data)

    # 强制新生成，不检查曾经的过程记录
    def upload_file_force(self, data):
        _PR = PR.getInstance()
        session_id = data.get('__sessionId__')
        if self.upload_to_server().getCode() == PR.Code_OK:
            self.upload_state_code_id = 'success'
            insert_upload_res = self.__insert_upload_info()
            if insert_upload_res.getCode() == PR.Code_ERROR:
                return _PR.setResult({'isUpload': False}).setCode(PR.Code_ERROR).setMsg('%s文件上传记录写入数据库故障' % self.fileName)
            if self.isToCdn:
                self.upload_to_cdn(session_id, insert_upload_res.getData())
        return _PR.setResult({'isUpload': True}).setCode(PR.Code_OK).setMsg('%s上传文件成功' % self.fileName)

    # 将文件保存到服务器上(本地)
    def upload_to_server(self):
        _PR = PR.getInstance()
        file_lock_name = self.fileName + str(self.chunkNumber)
        if not R.add_lock(key=file_lock_name, ttl=60):  # 添加文件上传阶段的redis锁
            return _PR.setCode(PR.Code_ERROR).setMsg('%s文件正在上传中' % self.fileName)
        _PR.setCode(PR.Code_ERROR)
        if self.createWriteTempFile():
            # 判断所有分片是否上传完成
            if self.chekIsSuccess():
                L.debug('the %s file  uploading finished , merge it ' % self.fileName)
                if self.mergeTempFile():
                    _PR.setCode(PR.Code_OK)
                    if self.delTempFile():
                        L.debug('delete the %s temp file success' % self.fileName)
                        msg = '上传文件成功,删除临时文件成功'
                    else:
                        L.debug('delete the %s temp file failed' % self.fileName)
                        msg = '上传文件成功,删除临时文件失败'
                else:
                    L.error('merge the %s temp file failed' % self.fileName)
                    msg = '上传文件失败，合并文件失败'
            else:
                L.debug('the %s file  still uploading' % self.fileName)
                msg = '检查临时文件完整性失败'
        else:
            L.debug('the %s file  still createWriteTempFile' % self.fileName)
            msg = '上传文件过程错误，写入块缓文件失败'
        R.release_lock(key=file_lock_name)  # 释放文件上传阶段的redis锁
        return _PR.setMsg(msg)

    # 将转移cdn的任务发布
    def upload_to_cdn(self, session_id, insert_data):
        # to fixed 2019年9月27日19:31:30 姚高超
        insert_data['to_cdn_state_code_id'] = '0'
        insert_data['toCdnConsumedTime'] = '0'
        SingleTableOpt.getInstance().setBO(UploadBo).setData(insert_data).update()  # 更新转移cdn进度信息
        # 写入发布任务上传cnd消息
        user_name = SessionDataOpt(session_id).getUserName()
        msg = Msg.getInstance().set_msg('发布上传%s文件至CDN任务' % self.fileName).set_user_name(user_name).set_par(insert_data).set_type_upload_to_cnd().json()
        RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)

    # 主要逻辑 组合
    # 0、在文件上传合并阶段添加redis
    # 1、文件完整性
    # 2、文件分步存储
    # def upload_file(self, data):  # 上传文件
    #     msg = ''
    #     session_id = data.get('__sessionId__')
    #     _PR = PR.getInstance()
    #     try:
    #         file_lock_name = self.fileName + str(self.chunkNumber)
    #         if not R.add_lock(key=file_lock_name, ttl=60):  # 添加文件上传阶段的redis锁
    #             return _PR.setResult({'isUpload': False}).setCode(PR.Code_ERROR).setMsg('存在相同的上传文件')
    #         res = False
    #         if self.createWriteTempFile():
    #             # 判断所有分片是否上传完成
    #             if self.chekIsSuccess():
    #                 L.debug('the %s file  uploading finished , merge it ' % self.fileName)
    #                 # 合并临时模块
    #                 if self.mergeTempFile():
    #                     res = True
    #                     if self.delTempFile():
    #                         L.debug('delete the %s temp file success' % self.fileName)
    #                     else:
    #                         L.debug('delete the %s temp file failed' % self.fileName)
    #                 else:
    #                     L.error('merge the %s temp file failed' % self.fileName)
    #                     msg = '上传文件失败，合并文件失败'
    #             else:
    #                 L.debug('the %s file  still uploading' % self.fileName)
    #         else:
    #             msg = '上传文件过程错误，写入块缓文件失败'
    #         R.release_lock(key=file_lock_name)  # 释放文件上传阶段的redis锁
    #         if res:
    #             self.upload_state_code_id = 'success'
    #             insert_re_code = self.__insertUploadInfo()
    #             if insert_re_code == '2':
    #                 return _PR.setResult({'isUpload': False}).setCode(PR.Code_WARNING).setMsg('存在相同的上传文件')
    #             elif insert_re_code == '0':
    #                 return _PR.setResult({'isUpload': False}).setCode(PR.Code_WARNING).setMsg('文件上传记录写入数据库故障')
    #             else:
    #                 pass
    #             # 发送转移到CDN中的任务到MQ 中
    #             if self.isToCdn:
    #                 insert_data = self.insertData.getData()
    #                 insert_data['to_cdn_state_code_id'] = '0'
    #                 insert_data['toCdnConsumedTime'] = '0'
    #                 SingleTableOpt.getInstance().setBO(UploadBo).setData(insert_data).update()
    #                 # 写入发布任务上传cnd消息
    #                 user_name = SessionDataOpt(session_id).getUserName()
    #                 msg = Msg.getInstance().set_msg('发布上传%s文件至CDN任务' % self.fileName).set_user_name(user_name).set_par(insert_data).set_type_upload_to_cnd().json()
    #                 RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
    #             return _PR.setResult({'isUpload': True}).setCode(PR.Code_OK).setMsg('上传文件成功')
    #         else:
    #             return _PR.setResult({'isUploadContinue': True}).setCode(PR.Code_OK).setMsg('上传中')
    #     except Exception as e:
    #         L.exception('upload file exception %s' % str(e))
    #         return _PR.setResult({'isUpload': False}).setCode(PR.Code_ERROR).setMsg(msg)

    # 文件下载
    def OAMP_downloadFile(self):
        pass

    # 文件下载通过CDN
    def OAMP_downloadFileByCDN(self):
        pass


def getInstance(data):
    return FileOpt(data)
