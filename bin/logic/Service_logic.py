#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import Logger
from bin.base.proc.trace import trace

from bin.logic.func.user import User
from bin.logic.func.user import VirtualIdentity
from bin.logic.func.setting.projectManage import ProjectUpdateConf
from bin.logic.func.setting.projectManage import Project
from bin.logic.func.setting.projectManage import ProjectTeamManage
from bin.logic.func.setting.projectManage import ProjectUpdate
from bin.logic.func.setting.projectManage import ProjectOptRecord
from bin.logic.func.setting.sysManage import RoleManage
from bin.logic.func.setting.sysManage import SysRouterManage
from bin.logic.func.setting.sysManage import SysUpdateManage
from bin.logic.func.setting import AgentSetting
from bin.logic.func.setting import ServerSetting
from bin.logic.func.setting import ToolSetting
from bin.logic.func.setting import CodeSetting
from bin.logic.func.setting import ServiceContainerConf
from bin.logic.func.common import Link
from bin.logic.func.upload import CdnFileUpDown
from bin.logic.func.upload import FileOpt
from bin.logic.func.upload import Upload
from bin.logic.func.record import MsgRecord
from bin.logic.func.record import MailRecord
from bin.logic.func.task import ServiceCheckTask

L = Logger.getInstance()


class Service_logic(object):
    '''
    @author:windyStreet
    @time:2018年3月6日17:39:42
    @version:V0.1.0
    @func:"工具信息设置插入"
    @param:data:{
       "tool_type_id":"tool_type_id”,string
       "tool_project_id":"tool_project_id”,string
       "tool_ip":"tool_ip",string
       "tool_port":"tool_port",string
       "tool_user_name":"tool_user_name",string
       "tool_password":"tool_password",string
       "_remarks":"_remarks",string
    } json (not null)
    @notice:""
    @PR:{
       "code": code
       "msg":msg
       "result":None
    }
    @return:PR
    '''

    # 新增代码表类型信息
    @trace()
    def OAMP_insert_code_type_info(self, data):
        return CodeSetting.getInstance().OAMP_insert_code_type_info(data)

    # 删除代码表类型信息

    @trace()
    def OAMP_delete_code_type_info(self, data):
        return CodeSetting.getInstance().OAMP_delete_code_type_info(data)

    # 更新代码表类型信息
    @trace()
    def OAMP_update_code_type_info(self, data):
        return CodeSetting.getInstance().OAMP_update_code_type_info(data)

    # 查询代码表表格信息
    @trace()
    def OAMP_search_code_info_list(self, data):
        return CodeSetting.getInstance().OAMP_search_code_info_list(data)

    # 插入代码表值数据
    @trace()
    def OAMP_insert_code_data(self, data):
        return CodeSetting.getInstance().OAMP_insert_code_data(data)

    # 更新代码表值数据
    @trace()
    def OAMP_update_code_data(self, data):
        return CodeSetting.getInstance().OAMP_update_code_data(data)

    # 删除代码表值数据
    @trace()
    def OAMP_delete_code_data(self, data):
        return CodeSetting.getInstance().OAMP_delete_code_data(data)

    # 查询代码数据列表【仅查询代码表值】
    @trace()
    def OAMP_search_code_data_list(self, data):
        return CodeSetting.getInstance().OAMP_search_code_data_list(data)

    #######################################
    # # 新增代码表信息
    # def OAMP_iCodeInfo(self, data):
    #     return CodeSetting.getInstance().OAMP_iCodeInfo(data)
    #
    # # 更新代码表类型信息
    # def OAMP_uCodeTypeInfo(self, data):
    #     return CodeSetting.getInstance().OAMP_uCodeTypeInfo(data)
    #
    # # 更新代码表值信息
    # def OAMP_uCodeValueInfo(self, data):
    #     return CodeSetting.getInstance().OAMP_uCodeValueInfo(data)
    #
    # # 获取代码表值信息
    # def OAMP_getCodeTypeInfo(self, data):
    #     return CodeSetting.getInstance().OAMP_getCodeTypeInfo(data)
    #
    # # 获取具体代码表值信息
    # def OAMP_getCodeValueInfo(self, data):
    #     return CodeSetting.getInstance().OAMP_getCodeValueInfo(data)
    #
    # # 获取同类代码表值信息
    # def OAMP_get_code_value_info_list(self, data):
    #     return CodeSetting.getInstance().OAMP_get_code_value_info_list(data)
    #

    # # 删除代码表信息
    # def OAMP_delete_code_info(self, data):
    #     return CodeSetting.getInstance().OAMP_delete_code_info(data)

    # 用户注册
    @trace()
    def OAMP_userRegister(self, data):
        return User.getInstance().OAMP_userRegister(data)

    # 用户的登录
    @trace()
    def OAMP_userLogin(self, data):
        return User.getInstance().OAMP_userLogin(data)

    # 用户的退出
    @trace()
    def OAMP_userQuit(self, data):
        return User.getInstance().OAMP_userQuit(data)

    # 查询用户信息列表
    @trace()
    def OAMP_search_user_info_list(self, data):
        return User.getInstance().OAMP_search_user_info_list(data)

    # 新增用户信息
    @trace()
    def OAMP_insert_user_info(self, data):
        return User.getInstance().OAMP_insert_user_info(data)

    # 修改用户信息
    @trace()
    def OAMP_update_user_info(self, data):
        return User.getInstance().OAMP_update_user_info(data)

    # 删除用户信息
    @trace()
    def OAMP_delete_user_info(self, data):
        return User.getInstance().OAMP_delete_user_info(data)

    # 创建虚拟用户
    @trace()
    def OAMP_create_virtual_identity(self, data):
        return VirtualIdentity.getInstance().OAMP_create_virtual_identity(data)

    # 查询项目信息
    @trace()
    def OAMP_search_project_list(self, data):
        return Project.getInstance().OAMP_search_project_list(data)

    # 新增项目信息
    @trace()
    def OAMP_insert_project_info(self, data):
        return Project.getInstance().OAMP_insert_project_info(data)

    # 更新项目信息
    @trace()
    def OAMP_update_project_info(self, data):
        return Project.getInstance().OAMP_update_project_info(data)

    # 删除项目信息
    @trace()
    def OAMP_delete_project_info(self, data):
        return Project.getInstance().OAMP_delete_project_info(data)


    # 获取项目code列表信息
    @trace()
    def OAMP_search_project_code_list(self, data):
        return Project.getInstance().OAMP_search_project_code_list(data)



    # 通过id查询项目信息
    @trace()
    def OAMP_search_project_info_by_id(self, data):
        return Project.getInstance().OAMP_search_project_info_by_id(data)

    # 查询项目关联服务器列表
    @trace()
    def OAMP_search_project_server_list(self, data):
        return Project.getInstance().OAMP_search_project_server_list(data)

    # 查询项目关联服务容器列表
    @trace()
    def OAMP_search_project_server_container_list(self, data):
        return Project.getInstance().OAMP_search_project_server_container_list(data)

    # project_update_conf 项目更新配置
    # 查询项目更新配置信息列表
    @trace()
    def OAMP_search_project_update_conf_info_list(self, data):
        return ProjectUpdateConf.getInstance().OAMP_search_project_update_conf_info_list(data)

    # 插入项目更新配置信息
    @trace()
    def OAMP_insert_project_update_conf_info(self, data):
        return ProjectUpdateConf.getInstance().OAMP_insert_project_update_conf_info(data)

    # 修改项目更新配置信息
    @trace()
    def OAMP_update_project_update_conf_info(self, data):
        return ProjectUpdateConf.getInstance().OAMP_update_project_update_conf_info(data)

    # 删除项目更新配置信息
    @trace()
    def OAMP_delete_project_update_conf_info(self, data):
        return ProjectUpdateConf.getInstance().OAMP_delete_project_update_conf_info(data)

    # 重建远程配置文件
    @trace()
    def OAMP_rebuild_remote_update_conf(self, data):
        return ProjectUpdateConf.getInstance().OAMP_rebuild_remote_update_conf(data)

    # 获取lib资源信息
    @trace()
    def OAMP_get_lib_res_info(self, data):
        return ProjectUpdate.getInstance().OAMP_get_lib_res_info(data)

    # 获取ResourceLib资源信息
    @trace()
    def OAMP_get_ResourceLib_res_info(self, data):
        return ProjectUpdate.getInstance().OAMP_get_ResourceLib_res_info(data)

    # 获取static资源信息
    @trace()
    def OAMP_get_static_res_info(self, data):
        return ProjectUpdate.getInstance().OAMP_get_static_res_info(data)

    # 项目操作
    # 查询项目操作记录列表
    @trace()
    def OAMP_search_project_opt_record_info_list(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_search_project_opt_record_info_list(data)

    # 标记版本
    @trace()
    def OAMP_project_remark_version(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_remark_version(data)

    # 全量更新
    @trace()
    def OAMP_project_full_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_full_update(data)

    # 标记更新
    @trace()
    def OAMP_project_remark_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_remark_update(data)

    # 标记取消
    @trace()
    def OAMP_project_remark_cancel(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_remark_cancel(data)

    # 增量更新
    @trace()
    def OAMP_project_increase_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_increase_update(data)

    # 静态文件更新
    @trace()
    def OAMP_project_static_file_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_static_file_update(data)

    # 项目回滚
    @trace()
    def OAMP_project_roll_back_update(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OAMP_project_roll_back_update(data)

    # 项目重启
    def OMAP_project_restart(self, data):
        return ProjectOptRecord.getInstance(data.get('project_id')).OMAP_project_restart(data)

    # project_team
    # 查询项目组信息列表
    @trace()
    def OAMP_search_project_team_info_list(self, data):
        return ProjectTeamManage.getInstance().OAMP_search_project_team_info_list(data)

    # 项目组

    # 新增项目组信息
    @trace()
    def OAMP_insert_project_team_info(self, data):
        return ProjectTeamManage.getInstance().OAMP_insert_project_team_info(data)

    # 修改项目组信息
    @trace()
    def OAMP_update_project_team_info(self, data):
        return ProjectTeamManage.getInstance().OAMP_update_project_team_info(data)

    # 删除项目组信息
    @trace()
    def OAMP_delete_project_team_info(self, data):
        return ProjectTeamManage.getInstance().OAMP_delete_project_team_info(data)

    # 查询项目组code列表
    @trace()
    def OAMP_search_project_team_code_list(self, data):
        return ProjectTeamManage.getInstance().OAMP_search_project_team_code_list(data)

    # role 角色管理
    # 查询角色信息列表
    @trace()
    def OAMP_search_role_info_list(self, data):
        return RoleManage.getInstance().OAMP_search_role_info_list(data)

    # 新增角色信息
    @trace()
    def OAMP_insert_role_info(self, data):
        return RoleManage.getInstance().OAMP_insert_role_info(data)

    # 修改角色信息
    @trace()
    def OAMP_update_role_info(self, data):
        return RoleManage.getInstance().OAMP_update_role_info(data)

    # 删除角色信息
    @trace()
    def OAMP_delete_role_info(self, data):
        return RoleManage.getInstance().OAMP_delete_role_info(data)

    # 查询角色代码列表信息
    @trace()
    def OAMP_search_role_code_list(self, data):
        return RoleManage.getInstance().OAMP_search_role_code_list(data)

    # 系统路由管理

    # 新增路由系统顶级节点
    @trace()
    def OAMP_insert_sys_router_top_node_info(self, data):
        return SysRouterManage.getInstance().OAMP_insert_sys_router_top_node_info(data)

    # 查询系统路由结构
    @trace()
    def OAMP_search_sys_router_tree_data(self, data):
        return SysRouterManage.getInstance().OAMP_search_sys_router_tree_data(data)

    # 查询系统路由信息列表
    @trace()
    def OAMP_search_sys_router_info_list(self, data):
        return SysRouterManage.getInstance().OAMP_search_sys_router_info_list(data)

    # 新增系统路由信息
    @trace()
    def OAMP_insert_sys_router_info(self, data):
        return SysRouterManage.getInstance().OAMP_insert_sys_router_info(data)

    # 更新系统路由信息
    @trace()
    def OAMP_update_sys_router_info(self, data):
        return SysRouterManage.getInstance().OAMP_update_sys_router_info(data)

    # 删除系统路由信息
    @trace()
    def OAMP_delete_sys_router_info(self, data):
        return SysRouterManage.getInstance().OAMP_delete_sys_router_info(data)

    # 添加路由权限
    def OMAP_add_router_authority(self, data):
        return SysRouterManage.getInstance().OMAP_add_router_authority(data)

    # 移除路由权限
    def OMAP_remove_router_authority(self, data):
        return SysRouterManage.getInstance().OMAP_remove_router_authority(data)

    # 工具管理
    # 查询工具列表信息
    @trace()
    def OAMP_search_tool_list(self, data):
        return ToolSetting.getInstance().OAMP_search_tool_list(data)

    # 删除工具信息
    @trace()
    def OAMP_delete_tool_info(self, data):
        return ToolSetting.getInstance().OAMP_delete_tool_info(data)

    # 新增工具信息
    @trace()
    def OAMP_insert_tool_info(self, data):
        return ToolSetting.getInstance().OAMP_insert_tool_info(data)

    # 修改工具信息
    @trace()
    def OAMP_update_tool_info(self, data):
        return ToolSetting.getInstance().OAMP_update_tool_info(data)

    # 获取工具信息
    @trace()
    def OAMP_get_tool_info(self, data):
        return ToolSetting.getInstance().OAMP_get_tool_info(data)

    # # 查询工具类型信息
    # def OAMP_getToolInfoByType(self, data):
    #     return ToolSetting.getInstance().OAMP_getToolInfoByType(data)

    ###################upload###################
    # 查询上传列表
    @trace()
    def OAMP_search_upload_list(self, data):
        return Upload.getInstance().OAMP_search_upload_list(data)

    # 重新启动转移至cdn任务
    @trace()
    def OAMP_retransmission(self, data):
        return Upload.getInstance().OAMP_retransmission(data)

    ###################upload###################
    # 文件上传

    @trace()
    def OAMP_uCdnUpload(self, data):
        return CdnFileUpDown.getInstance().CdnFileUpload(data)

        # 文件上传

    @trace()
    def OAMP_uploadFile(self, data):
        return FileOpt.getInstance(data).OAMP_uploadFile(data=data)

        # 文件下载

    @trace()
    def OAMP_downloadFile(self, data):
        return FileOpt.getInstance(data).OAMP_downloadFile()

        # 文件下载通过CDN

    @trace()
    def OAMP_downloadFileByCDN(self, data):
        return FileOpt.getInstance(data).OAMP_downloadFileByCDN()

    # 消息列表查询
    @trace()
    def OAMP_search_msg_info_list(self, data):
        return MsgRecord.getInstance().OAMP_search_msg_info_list(data=data)

    # open-falcon 邮件
    def mail_falcon(self, data):
        return MailRecord.getInstance().mail_falcon(data=data)

    # 查询服务器列表
    @trace()
    def OAMP_search_server_list(self, data):
        return ServerSetting.getInstance().OAMP_search_server_list(data=data)

    # 删除服务器信息
    @trace()
    def OAMP_delete_server_info(self, data):
        return ServerSetting.getInstance().OAMP_delete_server_info(data=data)

    # 新增服务器信息
    @trace()
    def OAMP_insert_server_info(self, data):
        return ServerSetting.getInstance().OAMP_insert_server_info(data=data)

    # 修改服务器信息
    @trace()
    def OAMP_update_server_info(self, data):
        return ServerSetting.getInstance().OAMP_update_server_info(data=data)

    # 通过项目id查询服务器列表
    @trace()
    def OAMP_search_server_list_by_project_id(self, data):
        return ServerSetting.getInstance().OAMP_search_server_list_by_project_id(data=data)

    # 查询服务容器列表
    @trace()
    def OAMP_search_service_container_list(self, data):
        return ServiceContainerConf.getInstance().OAMP_search_service_container_list(data=data)

    # 新增服务容器信息
    @trace()
    def OAMP_insert_service_container_info(self, data):
        return ServiceContainerConf.getInstance().OAMP_insert_service_container_info(data=data)

    # 更新服务容器信息
    @trace()
    def OAMP_update_service_container_info(self, data):
        return ServiceContainerConf.getInstance().OAMP_update_service_container_info(data=data)

    # 删除服务容器信息
    @trace()
    def OAMP_delete_service_container_info(self, data):
        return ServiceContainerConf.getInstance().OAMP_delete_service_container_info(data=data)

    # 查询代理信息列表
    @trace()
    def OAMP_search_agent_list(self, data):
        return AgentSetting.getInstance().OAMP_search_agent_list(data=data)

    # 删除代理信息
    @trace()
    def OAMP_delete_agent_info(self, data):
        return AgentSetting.getInstance().OAMP_delete_agent_info(data=data)

    # 新增代理信息
    @trace()
    def OAMP_insert_agent_info(self, data):
        return AgentSetting.getInstance().OAMP_insert_agent_info(data=data)

    # 修改代理信息
    @trace()
    def OAMP_update_agent_info(self, data):
        return AgentSetting.getInstance().OAMP_update_agent_info(data=data)

    # 查询代理配置树数据
    @trace()
    def OAMP_search_agent_conf_tree_data(self, data):
        return AgentSetting.getInstance().OAMP_search_agent_conf_tree_data(data=data)

    # 将 server 和 agent 关联
    @trace()
    def OAMP_linked_server_to_agent(self, data):
        return AgentSetting.getInstance().OAMP_linked_server_to_agent(data=data)

    # 取消 server 和 agent 关联
    @trace()
    def OAMP_unlinked_server_to_agent(self, data):
        return AgentSetting.getInstance().OAMP_unlinked_server_to_agent(data=data)

    # 查询未配置代理的服务器列表
    @trace()
    def OAMP_search_agent_server_list(self, data):
        return AgentSetting.getInstance().OAMP_search_agent_server_list(data=data)

    # 新增关联信息
    @trace()
    def OAMP_insert_link_info(self, data):
        return Link.getInstance().OAMP_insert_link_info(data=data)

    # 删除关联信息
    @trace()
    def OAMP_delete_link_info(self, data):
        return Link.getInstance().OAMP_delete_link_info(data=data)

    # 暂停服务检查
    @trace()
    def OAMP_pause_service_check(self, data):
        return ServiceCheckTask.getInstance().OAMP_pause_service_check(data=data)

    # 恢复服务检查
    @trace()
    def OAMP_resume_service_check(self, data):
        return ServiceCheckTask.getInstance().OAMP_resume_service_check(data=data)

    # 修改服务检查
    @trace()
    def OAMP_modify_service_check_info(self, data):
        return ServiceCheckTask.getInstance().OAMP_modify_service_check_info(data=data)

    # 重新生成服务检查
    @trace()
    def OAMP_recreate_service_check(self, data):
        return ServiceCheckTask.getInstance().OAMP_recreate_service_check(data=data)

    # 查询服务检查列表
    @trace()
    def OAMP_search_service_check_list(self, data):
        return ServiceCheckTask.getInstance().OAMP_search_service_check_list(data=data)

    # 运行服务检查
    @trace()
    def OAMP_run_service_check_task(self, data):
        return ServiceCheckTask.getInstance().OAMP_run_service_check_task(data=data)

    # 系统更新信息
    # 新增系统更新信息
    @trace()
    def OAMP_insert_sys_update_info(self, data):
        return SysUpdateManage.getInstance().OAMP_insert_sys_update_info(data=data)

    # 修改系统更新信息
    @trace()
    def OAMP_update_sys_update_info(self, data):
        return SysUpdateManage.getInstance().OAMP_update_sys_update_info(data=data)

    # 删除更新信息插入
    @trace()
    def OAMP_delete_sys_update_info(self, data):
        return SysUpdateManage.getInstance().OAMP_delete_sys_update_info(data=data)

    # 查询系统更新信息列表
    @trace()
    def OAMP_search_sys_update_info_list(self, data):
        return SysUpdateManage.getInstance().OAMP_search_sys_update_info_list(data=data)


def getInstance():
    return Service_logic()
