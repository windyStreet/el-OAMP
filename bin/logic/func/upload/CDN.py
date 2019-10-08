#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from ftplib import FTP
import os
from bin.base.log import Logger

L = Logger.getInstance('upload.log')


class CDN(object):
    def __init__(self, host=None, port=21, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = FTP()
        self.ftp.encoding = 'utf-8'
        if self.host is not None:
            self.connect = self.ftp.connect(host=self.host, port=self.port)
            self.instance = self.ftp.login(self.username, self.password)
        pass

    # ftp 判断目录是否存在
    def is_exist_dir(self, remote_dir):
        try:
            self.ftp.cwd(remote_dir)
            return True
        except Exception as e:
            # L.exception('ftp dir is not exist : %s ,exception info is %s' % (remote_dir, str(e)))
            return False

    # ftp 创建目录
    def mkdirs(self, remote_dir, des_dir=None):
        L.debug('ftp mkdirs : %s' % remote_dir)
        try:
            self.ftp.mkd(remote_dir)
            if des_dir is None or remote_dir == des_dir:
                return True
            else:
                self.mkdirs(remote_dir=des_dir)
        except Exception as e:
            if remote_dir == '/' or remote_dir == '\\':
                return False
            parent_dir = os.path.dirname(remote_dir)
            self.mkdirs(remote_dir=parent_dir, des_dir=remote_dir)
            L.exception('ftp create dir exception %s' % str(e))
            L.exception('ftp will create %s dir' % parent_dir)

    # 上传目录 代码未测试
    def upLoadFileTree(self, localDir, remoteDir):
        L.debug('upLoadFileTree ,localDir:%s, remoteDir:%s' % (str(localDir),str(remoteDir)))
        if os.path.isdir(localDir) == False:
            L.debug('upLoadFileTree: os.path.isdir(localDir) == False')
            return False
        localNames = os.listdir(localDir)
        # ftp 目录不存在则进行创建
        if self.is_exist_dir(remoteDir) == False:
            L.debug('upLoadFileTree: self.is_exist_dir(remoteDir) == False')
            self.mkdirs(remoteDir)
        self.ftp.cwd(remoteDir)
        for local in localNames:
            load_src = os.path.join(localDir, local)
            if os.path.isdir(load_src):
                remote_src = os.path.join(remoteDir, local)
                self.upLoadFileTree(localDir=load_src, remoteDir=remote_src)
            else:
                localFile = os.path.join(localDir, local)
                self.upLoadFile(localFile=localFile, remoteFile=local, remoteDir=remoteDir)
        self.ftp.cwd("..")
        return True

    # 上传文件
    def upLoadFile(self, localFile, remoteFile, remoteDir):
        if os.path.isfile(localFile) == False:
            L.error('upload file %s not exist' % localFile)
            return False
        try:
            if self.is_exist_dir(remoteDir) == False:
                self.mkdirs(remoteDir)
            self.ftp.cwd(remoteDir)
            file_handler = open(localFile, "rb")
            # self.ftp.storbinary('STOR %s' % remoteFile, file_handler, 8192, callback=self.upload_progress)
            self.ftp.storbinary('STOR %s' % remoteFile, file_handler, 8192)
            file_handler.close()
        except Exception as e:
            L.exception('upload to CDN %s file , failed exception %s ' % (localFile, str(e)))
            return False
        return True

    # def upload_progress(self, buf):
    # L.info('upload_progress buf is %s' % str(buf))


def getInstance(host=None, port=21, username=None, password=None):
    return CDN(host=host, port=port, username=username, password=password)
