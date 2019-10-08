# !-*- coding:utf-8 -*-

from mongoengine import *


class ExecFuncRecordBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    project = StringField()
    method = StringField()
    par = StringField()
    user_name = StringField()
    exec_count = IntField()
    msg = StringField()
