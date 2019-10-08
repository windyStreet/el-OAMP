# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(required=True, max_length=100)
#     fatherCode = StringField(max_length=100)


class ProjectUpdateConfBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    project_team_id = StringField(required=True)  # 项目组id
    project_id = StringField(required=True)  # 项目id

    update_structure = ListField()  # 更新结构
    update_ex_resource = ListField()  # 常用更新
    update_path = StringField()  # 更新文件路径
    remark_bak_path = StringField()  # 标记备份文件路径

    update_server_ip = StringField()  # 更新服务器ip
    update_server_port = StringField()  # 更新服务器端口
    agent_service_url = StringField()  # 代理服务地址
    update_share_bak_path = StringField()  # 更新备份路径
    update_share_conf_bak_path = StringField()  # 更新备份配置文件路径

    upstream_conf_file = StringField()  # upstream 文件位置
    redis_ip = StringField()
    redis_port = StringField()
    redis_password = StringField()

    project_update_summary = StringField()  # 项目更新简介
