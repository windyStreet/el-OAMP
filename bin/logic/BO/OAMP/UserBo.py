# !/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *


class UserBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    userName = StringField(required=True, max_length=100, unique=True)
    password = StringField(required=True, max_length=100)
    tel = IntField(required=True, max_length=20)
    email = StringField(required=True, max_length=100)
    nickName = StringField(required=True, max_length=100)
    roleId = ListField()  # 角色id
