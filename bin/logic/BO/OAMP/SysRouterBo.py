# !/usr/bin/env python
# !-*- coding:utf-8 -*-
from mongoengine import *


# 系统路由信息
class SysRouterBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    node_id = StringField(required=True)  # 节点id
    parent_id = StringField()  # 父节点id

    role_id = StringField(default='sys')  # 角色id
    project_id = StringField(default='sys')  # 项目id

    label = StringField()  # label
    router_show_name = StringField()  # 路由显示名称
    router_name = StringField()  # 路由名称
    router_path = StringField()  # 路由路径
    router_has_icon = StringField(default='false')  # 是否有图标
    router_icon_class = StringField()  # 图标样式
    router_icon_size = StringField()  # 大小
    order = DecimalField()  # 排序
