#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.SysRouterBo import SysRouterBo
from bin.base.sys import PR
from bin.base.data import TreeUntil
from bin.base.data import Data
import copy


class SysRouterManage(object):
    def __init__(self):
        pass

    # 新增路由系统顶级节点
    def OAMP_insert_sys_router_top_node_info(self, data):
        data['parent_id'] = None
        data['node_id'] = Data.getUUID()
        data['role_id'] = 'sys'
        data['project_id'] = 'sys'
        data['label'] = '系统路由'
        data['router_show_name'] = '系统路由'
        data['router_name'] = 'sys'
        data['router_path'] = '/'
        data['router_has_icon'] = 'false'
        data['order'] = 0
        return SingleTableOpt.getInstance().setBO(SysRouterBo).setData(data).insert()

    # 查询系统路由结构
    def OAMP_search_sys_router_tree_data(self, data):
        x = {
            'role_id': data.get('role_id', 'sys'),  # 角色id
            'project_id': data.get('project_id', 'sys')  # 项目id
        }
        _res = SingleTableOpt.getInstance().setBO(SysRouterBo).search(filters=x, par={'order': '+order'})
        if _res.is_results_not_none():
            tree_ins = TreeUntil.getInstance({})
            for re in _res.getData():
                tree_ins.add_node(re)
            result = tree_ins.json()
            return PR.getInstance().setCode(PR.Code_OK).setResult(result).setMsg('查询系统路由结构成功')
        else:
            return PR.getInstance().setCode(PR.Code_OK).setResult(None).setMsg('查询系统路由结构,未查询到系统结构')

    # 查询系统路由信息列表
    def OAMP_search_sys_router_info_list(self, data, only=[]):
        x = {
            'id': data.get('_id'),
            'role_id': data.get('role_id', 'sys'),  # 角色id
            'project_id': data.get('project_id', 'sys'),  # 项目id
            'node_id': data.get('node_id'),  # 当前节点id
            'parent_id': data.get('parent_id'),  # 父节点id
            'router_has_child': data.get('router_has_child'),  # 父节点id
            'router_show_name__contains': data.get('router_show_name'),
            'router_name__contains': data.get('router_name'),
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else ''
        }
        return SingleTableOpt.getInstance().setBO(SysRouterBo).search(filters=x, par=data, only=only)

    # 修改父节点状态信息
    def __update_parent_node_info(self, data, opt):
        parent_id = data.get('parent_id')
        # 查询node_id == parent_id 的数据，将其更新为对应状态 router_has_child
        search_data = {
            'node_id': parent_id,
        }
        res_pr = SingleTableOpt.getInstance().setBO(SysRouterBo).search(filters=search_data)
        if res_pr.is_results_not_none():  # 结果不为空的情况下
            for item in res_pr.getData():  # 循环当前结果
                if opt == 'insert' or opt == 'update':  # 操作类型为插入或者更新时，更改上级节点为存在下级节点
                    item['router_has_child'] = 'true'
                if opt == 'delete':  # 操作类型为删除时，更改上级节点为不存在下级节点
                    item['router_has_child'] = 'false'
                SingleTableOpt.getInstance().setBO(SysRouterBo).setData(item).update()

    # 新增系统路由信息
    def OAMP_insert_sys_router_info(self, data):
        data['node_id'] = Data.getUUID()
        data['role_id'] = data.get('role_id', 'sys')  # 角色id
        data['project_id'] = data.get('project_id', 'sys')  # 项目id
        self.__update_parent_node_info(data, 'insert')
        return SingleTableOpt.getInstance().setBO(SysRouterBo).setData(data).insert()

    # 更新系统路由信息
    def OAMP_update_sys_router_info(self, data):
        self.__update_parent_node_info(data, 'update')
        return SingleTableOpt.getInstance().setBO(SysRouterBo).setData(data).update()

    def _check_is_has_child(self, data):
        # 查询子节点
        x = {
            'parent_id': data.get('node_id'),
            'role_id': 'sys' if data.get('role_id') is None else data.get('role_id'),  # 角色id
            'project_id': 'sys' if data.get('project_id') is None else data.get('project_id'),  # 项目id
        }
        _res = SingleTableOpt.getInstance().setBO(SysRouterBo).search(filters=x)
        return _res.is_results_not_none()

    # 删除系统路由信息
    def OAMP_delete_sys_router_info(self, data):
        # 检查是否有子节点
        if 'value' in data.keys():
            data = data.get('value')
        if self._check_is_has_child(data=data):
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult(None).setMsg('删除节点存在子节点')
        else:
            self.__update_parent_node_info(data, 'delete')
            return SingleTableOpt.getInstance().setBO(SysRouterBo).setData(data).delete()

    # 添加路由权限
    def OMAP_add_router_authority(self, data):
        # 删除老的路由权限
        # 生成新的路由权限
        try:
            role_id = 'sys' if data.get('role_id') is None else data.get('role_id')
            project_id = 'sys' if data.get('project_id') is None else data.get('project_id')
            origin_bean = data.get('data')
            origin_node_ids = []
            if role_id == 'sys':
                return PR.getInstance().setCode(PR.Code_ERROR).setResult({'is_success': 'false'}).setMsg('角色信息参数未传递')
            x = {
                'role_id': role_id,
                'project_id': project_id,
            }
            old_res = SingleTableOpt.getInstance().setBO(SysRouterBo).search(filters=x)
            if old_res.is_results_not_none():
                for old_data in old_res.getData():
                    for origin_data in origin_bean:
                        if origin_data.get('value').get('node_id') == old_data.get('node_id'):
                            origin_node_ids.append(old_data.get('node_id'))
            for i_data in origin_bean:
                i_bean = i_data.get('value')
                if i_bean is None:
                    return PR.getInstance().setCode(PR.Code_ERROR).setResult({'is_success': 'false'}).setMsg('传递原路由权限信息错误')
                if i_bean.get('node_id') in origin_node_ids:
                    continue
                i_bean['_id'] = Data.getUUID()
                i_bean['role_id'] = role_id
                i_bean['project_id'] = project_id
                i_re = SingleTableOpt.getInstance().setBO(SysRouterBo).setData(i_bean).insert()
                if not i_re.is_result_not_none():
                    return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': 'false'}).setMsg('新增路由权限信息失败')
            return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': 'true'}).setMsg('新增路由权限信息成功')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': 'false'}).setMsg(str(e))

    # 移除路由权限
    def OMAP_remove_router_authority(self, data):
        # 删除路由权限
        try:
            delete_bean = data.get('data')
            for d_data in delete_bean:
                d_bean = d_data.get('value')
                if d_bean is None:
                    return PR.getInstance().setCode(PR.Code_ERROR).setResult({'is_success': 'false'}).setMsg('传递原路由权限信息错误')
                del_re = SingleTableOpt.getInstance().setBO(SysRouterBo).setData(data=d_bean).delete()
                if not del_re.is_result_not_none():
                    return PR.getInstance().setCode(PR.Code_ERROR).setResult({'is_success': 'false'}).setMsg('移除原路由权限失败')
            return PR.getInstance().setCode(PR.Code_OK).setResult({'is_success': 'true'}).setMsg('移除原路由权限成功')
        except Exception as e:
            return PR.getInstance().setCode(PR.Code_EXCEPTION).setResult({'is_success': 'false'}).setMsg(str(e))


def getInstance():
    return SysRouterManage()
