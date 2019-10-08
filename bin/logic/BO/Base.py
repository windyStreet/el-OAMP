#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *
from datetime import datetime


class BaseBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
