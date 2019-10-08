# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(required=True, max_length=100)
#     fatherCode = StringField(max_length=100)


class RoleBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    role_name = StringField(max_length=50)  # 角色名称
    role_type_code_id = StringField()  # 角色类型 1. 系统设置角色 2.自定义角色
    project_id = StringField()  # 项目id
    role_summary = StringField()  # 角色简介
