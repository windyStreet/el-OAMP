# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# 服务器信息
class ServiceCheckBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)
    service_project_id = StringField()  # 服务项目id
    service_container_id = StringField()  # 服务容器id
    service_name = StringField()  # 服务名称
    service_ips = ListField()  # 服务ips
    service_port = StringField()  # 服务端口
    service_state_code_id = StringField()  # 服务运行状态
    service_check_rate = IntField()  # 服务检查频率（单位 s）

    service_check_step = ListField()  # 服务检查步骤 [{'url':'','par':'','result':''}]
    service_check_url = ListField()  # 服务检查地址
    service_check_par = StringField()  # 服务检查参数
    service_check_result = StringField()  # 服务检查结果

    service_check_state_code_id = StringField()  # 服务检查状态
    service_check_last_result = StringField()  # 服务最后一次检查结果
    service_check_count = IntField()  # 服务检查累计次数
    service_check_continued_error_count = IntField()  # 服务检查持续累计错误次数【变为正常，即恢复为0】
    service_check_error_count = IntField()  # 服务检查累计错误次数
    service_check_threshold = IntField()  # 检查次数阈值 默认为3
