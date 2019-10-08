# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# 服务器信息
class ServiceContainerBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    belong_to_server_id = StringField(max_length=100)  # 所属服务器id
    service_container_name = StringField()  # 服务容器名称
    service_container_type_code_id = StringField()  # 服务容器类型
    service_container_path = StringField()  # 服务容器路径
    service_container_port = StringField()  # 服务容器端口
    service_container_user = StringField()  # 服务容器用户
    service_container_password = StringField()  # 服务容器密码
    start_container_command = StringField()  # 启动服务容器命令
    stop_container_command = StringField()  # 关闭服务容器命令
    reload_container_command = StringField()  # 重载服务容器命令
    service_container_state_code_id = StringField()  # 服务容器状态 .... 没想好这个怎么玩
