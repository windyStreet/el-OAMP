#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin import init
from bin.base.sys import PR
from bin.base.sys.Bean import Bean
from bin.base.db.MongoEng import MongoEng
from mongoengine import Q
from bin.logic.BO.OAMP.UserBo import UserBo
from bin.base.data import Data
from bin.base.sys.Session import SessionDataOpt
from bin.base.log import Logger
from bin.base.sys import SingleTableOpt
from bin.logic import Inner_logic
from bin.base.data import NavigationTreeUntil

L = Logger.getInstance()


class User(object):

    def OAMP_userRegister(self, data):
        _PR = PR.getInstance()
        _sessionId = data.get('__sessionId__')
        insertBean = Bean().getInsertBean(data, classBo=UserBo)
        MongoEng(init.ROOT_DB_DS).getCollection()
        bo = UserBo(**insertBean)
        res = bo.save()
        result = Data.removeJsonAtrr(res._data, ['password'])
        if res is not None:
            return _PR.setResult(result).setCode(PR.Code_OK).setMsg('注册成功')
        else:
            result['isLogin'] = 1
            # 注册成功，默认登录
            SessionDataOpt(sessionId=_sessionId).setSession(value=result, ex=init.DEFAULT_SESSION_EXPIRE_TIME)
            return _PR.setResult(result).setCode(PR.Code_ERROR).setMsg('注册失败')

    def OAMP_userLogin(self, data):
        _PR = PR.getInstance()
        _sessionId = data.get('__sessionId__')
        if data.get('userName', None) is None or data.get('password', None) is None:
            return _PR.setResult({}).setCode(PR.Code_ERROR).setMsg('未输入用户名或密码')
        x = {
            'userName': data.get('userName', "_error_"),
            'password': data.get('password', '__-1__'),
        }
        f = Q(**x)
        MongoEng(init.ROOT_DB_DS).getCollection()
        res = UserBo.objects.filter(f).first()
        if res is None:
            return _PR.setResult(None).setCode(PR.Code_OK).setMsg('用户名或密码错误')
        else:
            result = Data.removeJsonAtrr(res._data, ['password'])
            result['isLogin'] = 1
            # 测试设置10s过期，观察结果 正式为30分钟
            SessionDataOpt(sessionId=_sessionId).setSession(value=result, ex=init.DEFAULT_SESSION_EXPIRE_TIME)
            return _PR.setResult(result).setCode(PR.Code_OK).setMsg('登录成功')

    def OAMP_userQuit(self, data):
        _PR = PR.getInstance()
        # 清除用户session 以及redis信息
        _sessionId = data.get('__sessionId__')
        isQuit = SessionDataOpt(sessionId=_sessionId).delSession()
        return _PR.setResult({'isQuit': isQuit}).setCode(PR.Code_OK).setMsg('退出成功')

    # 查询用户信息列表
    def OAMP_search_user_info_list(self, data):
        x = {
            'createTime__gte': data.get('createTime')[0] if data.get('createTime') is not None and len(data.get('createTime')) >= 1 else '',
            'createTime__lt': data.get('createTime')[1] if data.get('createTime') is not None and len(data.get('createTime')) >= 2 else '',
            'userName__contains': data.get('userName', None),
            'tel__contains': data.get('tel', None)
        }
        return SingleTableOpt.getInstance().setBO(UserBo).search(filters=x, par=data)

    # 新增用户信息
    def OAMP_insert_user_info(self, data):
        return SingleTableOpt.getInstance().setBO(UserBo).setData(data=data).insert()

    # 修改用户信息
    def OAMP_update_user_info(self, data):
        return SingleTableOpt.getInstance(bo=UserBo, data=data).update()

    # 删除用户信息
    def OAMP_delete_user_info(self, data):
        return SingleTableOpt.getInstance(bo=UserBo, data=data).delete()

    # 查询用户导航信息
    # par roleId[arr]
    def OAMP_search_user_navigation(self, data):
        # 查询角色关联的权限数据
        # 组合数据结构
        # 返回数据
        roleIds = data.get('roleId')
        if roleIds is None:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult(None).setMsg('请系统管理员为当前用户配置权限')
        only = ['id', 'node_id', 'parent_id', 'router_has_child', 'router_has_icon', 'router_icon_class', 'router_show_name', 'router_path']
        nav_tree_ins = NavigationTreeUntil.getInstance()
        for roleId in roleIds:
            router_info_res = Inner_logic.getInstance().search_sys_router_info_list({'role_id': roleId}, only)
            if router_info_res.is_results_not_none():
                for item in router_info_res.getData():
                    nav_tree_ins.add_node(item)
        result = {
            'router_tree':nav_tree_ins.json(),
            'router_list':nav_tree_ins.get_filter_node()
        }
        return PR.getInstance().setCode(PR.Code_OK).setResult(result).setMsg("功能待完善")
        # return PR.getInstance().setCode(PR.Code_OK).setResult(None).setMsg("功能待完善")


def getInstance():
    return User()
