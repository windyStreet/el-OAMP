#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *
from datetime import datetime
from bin.base.data import Data


class Grade(EmbeddedDocument):
    ''' 内嵌文档 '''
    name = StringField(required=True)
    score = FloatField(required=True)


SEX_CHOICES = (('female', '女'),
               ('male', '男'))


class Odm(Document):
    ''' ODM 示例'''
    id = StringField(required=True, default=Data.getUUID(), primary_key=True)
    createTime = DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    updateTime = DateTimeField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    name = StringField(required=True, max_length=200)
    age = IntField(required=True)
    sex = StringField(required=True, choices=SEX_CHOICES)
    grade = FloatField()
    grads = ListField(EmbeddedDocumentField(Grade))
