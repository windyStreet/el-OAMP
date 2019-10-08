# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *
from bin.logic.BO.Base import BaseBo


class UploadBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    upload_project_id = StringField(max_length=100)  # 项目
    to_cdn_rule_code_id = StringField()  # 转移cdn目录规则
    upload_mode_code_id = StringField()  # # 通用 1 、强制2 、覆盖 3 上传模式
    cdnRootPath = StringField()  # CDN 根路径

    fileName = StringField(max_length=200)  # 文件名称
    filePath = StringField()  # 文件存储路径
    fileCdnPath = StringField()  # 文件CDN存储地址
    fileSize = StringField()  # 文件大小
    upload_state_code_id = StringField(required=True)  # 上传状态
    reliability_state_code_id = StringField(default='0')  # 0  不可用  100 可靠 90 需检验 80 疑似故障 70 故障 50 不可靠
    reliable_risk = IntField(default=0)  # 可靠风险
    isToCdn = BooleanField()  # 是否转移至CDN
    to_cdn_state_code_id = StringField()  # # 转移CDN状态   # 0 转移等待 1 转移中 2 转移成功 3 转移失败 4 转移异常【该值存放于代码表中】
    toCdnConsumedTime = StringField()  # 转移CDN已耗时时间
    downLoadCount = IntField(default=0)  # 下载次数 [可选]
    cdnDownLoadCount = IntField(default=0)  # cdn下载次数 [可选]
