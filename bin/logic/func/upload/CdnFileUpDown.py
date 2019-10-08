#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
class CdnFileUpDown(object):


    def CdnFileUpload(self):

        # fields = self.request.body
        # files = self.requtest.files
        # chunkNumber = fields['chunkNumber'] #当前块的次序
        # chunkSize = fields['chunkSize']     #分块大小
        # totalSize = fields['totalSize']     #文件总大小
        # identifier = self.cleanIdentifier(fields['identifier']) #文件唯一标识
        # filename = fields['filename']       #文件名

        identifier = self.request.body_arguments.identifier  # 文件唯一标识
        chunkNumber = self.request.body_arguments.chunkNumber  # 当前块的次序

        filename = '%s%s' % (identifier, chunkNumber)  # 构造该分片的唯一标识符
        upload_file = self.request.files['file']
        upload_file.save('./upload/%s' % filename)  # 保存分片到本地

    def cleanIdentifier(self, identifier):
        return identifier.replace("/ [ ^ 0 - 9A - Za - z_ -] / g", '')

    def upload_success(self):  # 按序读出分片内容，并写入新文件
        target_filename = self.request.args.get('filename')  # 获取上传文件的文件名
        task = self.request.get('task_id')  # 获取文件的唯一标识符
        chunk = 0  # 分片序号
        with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
            while True:
                try:
                    filename = './upload/%s%d' % (task, chunk)
                    source_file = open(filename, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                except IOError as msg:
                    break

                chunk += 1
                os.remove(filename)  # 删除该分片，节约空间


def getInstance():
    return CdnFileUpDown()


