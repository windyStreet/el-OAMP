# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *

class SysUpdateBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    version_number = StringField(required=True, max_length=20)
    version_update_time = StringField(required=True, max_length=20)
    version_content = ListField(StringField(required=True, max_length=5000),required=True)




