# !/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *


class ToolBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    tool_type_code_id = StringField(required=True)
    toolName = StringField(required=True, max_length=50, unique=True)
    toolPort = IntField(max_length=10)
    toolHost = StringField(max_length=100)
    toolUser = StringField(max_length=100)
    toolPassword = StringField(max_length=100)
    toolContext = StringField(max_length=100)
    toolRootPath = StringField()
    tool_project_id = StringField(max_length=100)
