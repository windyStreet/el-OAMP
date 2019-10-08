# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# 关联表
# a 关联 b
class LinkBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    link_id = StringField()  # 关联id
    linked_id = StringField()  # 被关联id
    link_type_code_id = StringField()  # 关联类型
