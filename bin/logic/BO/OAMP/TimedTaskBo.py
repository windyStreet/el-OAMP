# !/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *


class TimedTaskBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

