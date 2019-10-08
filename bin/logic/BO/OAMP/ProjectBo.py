# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(required=True, max_length=100)
#     fatherCode = StringField(max_length=100)


class ProjectBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    project = StringField(max_length=100, unique=True)  # 项目 'YXYBBTEST',
    project_name = StringField(max_length=100)  # 项目名称 '保宝网测试',
    project_context = StringField(max_length=100)  # 项目上下文 'YXYBBTEST',
    project_type_code_id = StringField(max_length=50)  # 项目类型code值
    project_env_code_id = StringField(max_length=50)  # 项目环境code值

    project_state_code_id = StringField(max_length=50)  # 项目运行状态code值 # EXCEPTION 异常中 RUNNING 运行中 关闭 冻结 归档 INCREASE_UPDATE 增量更新中 	FULL_UPDATE 全量更新中 REMARK_UPDATE 标记更新中 REPLACE_RES 替换资源中 ROLL_BACK 回滚中 RESTART 重启中

    project_service_state_code_id = StringField(max_length=50)  # 项目服务运行状态code值
    project_container_status = StringField()  # 3/2/5/10  3个错误 2个不检查 5个正常 共计10个

    project_version = StringField(max_length=20, default='1')  # 项目版本: 'v1.0.35',
    project_last_version = StringField(max_length=20, default='1')  # 项目上个版本: 'v1.0.35',
    project_last_opt_summary = StringField(max_length=20, default='1')  # 上次操作描述
    project_team_id = StringField(max_length=32)  # 项目团队id
    project_check_service = StringField()  # 项目检测服务
    project_check_result = StringField()  # 项目检测服务预期结果
    project_default_root_path = StringField()  # 项目默认根路径
