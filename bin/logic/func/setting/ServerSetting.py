#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.data import Data
from bin.base.sys import PR
from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.ServerBo import ServerBo
from bin.logic.func.common import Link


class ServerSetting(object):
    def __init__(self):
        pass

    # '''
    #     server_name = StringField(max_length=100)  # 服务器名称
    #     server_no = StringField(max_length=50)  # 服务器编号
    #     server_shelf_time = StringField(max_length=100)  # 服务器上架时间
    #     server_down_time = StringField(max_length=100)  # 服务器下架时间
    #     server_state_code_id = StringField()  # 服务器状态 未上架 已上架 使用中 下架 退役
    #     server_outer_ip = ListField()  # 外网ip
    #     server_inner_ip = ListField()  # 内网ip
    # '''
    # 查询服务器列表
    def OAMP_search_server_list(self, data):
        x = {
            'server_name__contains': data.get('server_name'),
            'server_no__contains': data.get('server_no'),
        }
        return SingleTableOpt.getInstance().setBO(ServerBo).search(filters=x, par=data)

    # 删除服务器信息
    def OAMP_delete_server_info(self, data):
        return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).delete()

    # 新增服务器信息
    def OAMP_insert_server_info(self, data):
        # 新增 服务器
        if data.get('is_agent') == 'true':
            uuid = Data.getUUID()
            data['_id'] = uuid
            data['agent_id'] = uuid
            data['agent_server_id'] = None
        else:
            data['agent_server_id'] = None
            data['agent_motor_room'] = None
        return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).insert()

    # 修改服务器信息
    def OAMP_update_server_info(self, data):
        search_res = SingleTableOpt.getInstance().setBO(ServerBo).setData(data).search()
        if search_res.getCode() == PR.Code_OK:
            search_data = search_res.getData()
            if search_data.get('is_agent') != 'true' and data.get('is_agent') == 'true':
                data['agent_id'] = search_data.get('_id')
                data['agent_server_id'] = None
            return SingleTableOpt.getInstance().setBO(ServerBo).setData(data).update()
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('服务器信息已不存在')

    # 通过项目id查询服务器列表
    def OAMP_search_server_list_by_project_id(self, data):
        project_id = data.get('project_id', None)
        if project_id is None:
            return PR.getInstance().setCode(PR.Code_PARERROR).setResult({}).setMsg('par error')
        _par = {
            'link_id': project_id,
            'link_type_code_id': '1'
        }
        _link_res = Link.getInstance().OAMP_search_link_info_by_link_id(data=_par)
        result = []
        if _link_res is not None and _link_res.getCode() == PR.Code_OK and _link_res.getData() is not None:
            for link_info in _link_res.getData():
                linked_id = link_info.get('linked_id')  # project_id
                _server_re = SingleTableOpt.getInstance().setBO(ServerBo).setData({'_id': linked_id}).search()
                if _server_re.is_result_not_none():
                    res = _server_re.getData()
                    res['link_info_id'] = link_info.get('_id')
                    result.append(res)
        return PR.getInstance().setCode(PR.Code_OK).setResult({"data": result}).setMsg('查询成功')


def getInstance():
    return ServerSetting()
