# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(required=True, max_length=100)
#     fatherCode = StringField(max_length=100)


class CodeBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    code = StringField(required=True, max_length=100)  # goods                     food
    codeName = StringField(required=True, max_length=100)  # 商品                       食物
    codeId = StringField(max_length=100)  # 1         2               1       2
    codeValue = StringField(max_length=100)  # 食物       百货           苹果      橘子
    fatherCode = StringField(max_length=100)  # goods
    isCodeType = BooleanField(required=True, default=0)
