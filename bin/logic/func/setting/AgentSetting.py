#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.sys import PR
from bin.base.sys import SingleTableOpt
from bin.base.data.echart import TreeData
from bin.logic.BO.OAMP.ServerBo import ServerBo


class AgentSetting(object):
    def __init__(self):
        pass

    # agent_server_id = StringField()  # 代理服务器id
    # agent_name = StringField(max_length=100)  # 服务器名称
    # agent_outer_ip = StringField(max_length=50)  # 代理外网ip
    # agent_inner_ip = StringField(max_length=50)  # 代理内网ip
    # agent_location = StringField()  # 代理服务器位置
    # agent_motor_room = StringField()  # 代理机房
    # agent_network_area = StringField  # 代理网络区域【代理网段】
    # agent_safety_code = StringField()  # 代理安全码

    # 查询代理信息列表
    def OAMP_search_agent_list(self, data):
        x = {
            'server_name': data.get('server_name'),
            'is_agent': 'true'
        }
        return SingleTableOpt.getInstance().setBO(ServerBo).search(filters=x, par=data)

    # 删除代理信息
    def OAMP_delete_agent_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).delete()

    # 新增代理信息
    def OAMP_insert_agent_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).insert()

    # 修改代理信息
    def OAMP_update_agent_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).update()

    # 查询代理配置树数据
    def OAMP_search_agent_conf_tree_data(self, data):
        # agent 信息存在，查询所代理的服务器信息
        x = {
            'agent_id': data.get('agent_id'),
        }
        server_list = SingleTableOpt.getInstance().setBO(ServerBo).search(filters=x)

        if server_list.getCode() == PR.Code_OK and server_list.getData() is not None:
            server_list = server_list.getData()
            tree = TreeData.getInstance()
            for server in server_list:
                tree.set_node_data(id=server.get('_id'), pid=server.get('agent_server_id', None), name=server.get('server_name'), value=server.get('server_outer_ip') + ' |  ' + server.get('server_inner_ip'))
            return PR.getInstance().setCode(PR.Code_OK).setResult(tree.json()).setMsg('获取代理结构树成功')
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('代理服务器信息不存在')

    # 查询未配置代理的服务器列表
    def OAMP_search_agent_server_list(self, data):
        x = {
            'server_name__contains': data.get('server_name'),
            'server_inner_ip__contains': data.get('server_inner_ip'),
            'agent_id': None
        }
        return SingleTableOpt.getInstance().setBO(ServerBo).search(filters=x, par=data)

    # 将 server 和 agent 关联
    def OAMP_linked_server_to_agent(self, data):
        __sessionId__ = data.get('__sessionId__')
        agent_id = data.get('agent_id')
        agent_server_id = data.get('agent_server_id')
        server_list = data.get('server_list')
        for server in server_list:
            update_data = server
            update_data['agent_id'] = agent_id
            update_data['agent_server_id'] = agent_server_id
            res = SingleTableOpt.getInstance().setBO(ServerBo).setData(update_data).set_session(__sessionId__).update()
            if res.getCode() == PR.Code_OK:
                continue
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setResult({'success': False}).setMsg('关联agent失败')
        return PR.getInstance().setCode(PR.Code_OK).setResult({'success': True}).setMsg('关联agent成功')

    # 取消 server 和 agent 关联
    def OAMP_unlinked_server_to_agent(self, data):
        __sessionId__ = data.get('__sessionId__')
        res = SingleTableOpt.getInstance().setBO(ServerBo).setData(data).search()
        if res.getCode() == PR.Code_OK:
            update_bean = res.getData()
            update_bean['agent_id'] = None
            update_bean['agent_server_id'] = None
            u_res = SingleTableOpt.getInstance().setBO(ServerBo).setData(update_bean).set_session(__sessionId__).update()
            if u_res.getCode() == PR.Code_OK:
                return PR.getInstance().setCode(PR.Code_OK).setResult({'success': True}).setMsg('取消关联成功')
        return PR.getInstance().setCode(PR.Code_ERROR).setResult({'success': False}).setMsg('取消关联失败')


def getInstance():
    return AgentSetting()
