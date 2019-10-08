# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# 服务器信息
class ServerBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    server_name = StringField(max_length=100)  # 服务器名称
    server_no = StringField(max_length=50)  # 服务器编号
    server_shelf_time = StringField(max_length=100)  # 服务器上架时间
    server_down_time = StringField(max_length=100)  # 服务器下架时间
    server_state_code_id = StringField()  # 服务器状态 未上架 已上架 使用中 下架 退役
    server_outer_ip = StringField()  # 外网ip
    server_inner_ip = StringField()  # 内网ip
    server_location = StringField()  # 服务器地址
    serve_ips = ListField()  # ip

    is_agent = StringField()  # 是否为代理
    agent_id = StringField()  # 代理id
    agent_server_id = StringField()  # 代理服务器id
    agent_motor_room = StringField()  # 代理机房
    agent_network_area = StringField()  # 代理网络区域【代理网段】
    agent_safety_code = StringField()  # 代理安全码
