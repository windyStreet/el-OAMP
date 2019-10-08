# !/usr/bin/env python
# !-*- coding:utf-8 -*-

from mongoengine import *


# class CodeInfo(EmbeddedDocument):
#     # ''' 内嵌文档 '''
#     codeId = StringField(required=True, max_length=100)
#     codeValue = StringField(required=True, max_length=100)
#     fatherCode = StringField(max_length=100)

# 项目操作记录
class ProjectOptRecordBo(Document):
    id = StringField(required=True, primary_key=True)
    createTime = StringField()
    updateTime = StringField()
    creator = StringField(max_length=100)
    updater = StringField(max_length=100)
    remark = StringField(max_length=2000)

    project_opt_user_name = StringField()  # 项目操作人
    project_id = StringField(required=True)  # 项目id
    project_opt_version = StringField(required=True)  # 操作项目版本号
    project_opt_last_version = StringField()  # 项目操作上个版本号
    project_opt_type_code_id = StringField(required=True)  # 项目操作类型  0修改全量资源、1重启、2标记、3资源替换、4标记更新、5全量更新、6增量更新、7回滚、8标记取消
    project_opt_summary = StringField(required=True)  # 操作说明

    project_opt_res_info = ListField()  # 项目操作资源信息
    project_opt_start_time = StringField()  # 项目操作开始时间
    project_opt_end_time = StringField()  # 项目操作结束时间
    is_opt_success = StringField()  # 操作结果 失败 成功
    remote_server_ip = ListField()  # 远程服务器ip
    remote_exec_count = IntField()  # 远程执行次数
    remote_exec_result = ListField()  # 远程执行结果
    exec_state_code_id = StringField(default='0')  # 执行状态  # 0未执行 1执行中 2执行结束 3 未知# 默认未执行
    is_able_rollback = StringField(default='0')  # 是否可回滚 默认不可回滚
