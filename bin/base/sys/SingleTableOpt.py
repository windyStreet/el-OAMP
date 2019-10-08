#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bin.base.sys import PR
from bin.base.db.MongoEng import MongoEng
from bin.base.sys.Bean import Bean
from mongoengine import Q
from bin import init

# 查询默认最大值
DEFAULT_SEARCH_MAX_SIZE = 10000


class SingleTableOpt(object):
    def __init__(self, ds, bo, data):
        self.BO = None if bo is None else bo
        self.data = {} if data is None else data
        self.ds = ds
        self.__session__ = None

    def set_session(self, session):
        self.data['__sessionId__'] = session
        return self

    def setBO(self, Bo):
        self.BO = Bo
        return self

    def setData(self, data):
        self.data = data
        return self

    def setDataSource(self, ds):
        self.ds = ds
        return self

    def delete(self):
        _PR = PR.getInstance()
        if self.BO is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用删除，未设置修改对象")
        if self.data is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用删除，未给出参数")
        if self.ds is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用删除，未设置数据源")
        else:
            try:
                if self.data.get('_id') is None:
                    return _PR.setResult(self.data).setCode(PR.Code_PARERROR).setMsg('通用删除，参数缺失')
                MongoEng(self.ds).getCollection()
                x = {
                    'id': self.data.get('_id')
                }
                f = Q(**Bean().getSearchBean(x))
                res = self.BO.objects.filter(f).delete()
                if res == 1:
                    return _PR.setResult(res).setCode(PR.Code_OK).setMsg('通用删除，删除成功')
                else:
                    return _PR.setResult(res).setCode(PR.Code_WARNING).setMsg('通用删除,未找到删除数据')
            except Exception as e:
                return _PR.setResult(None).setCode(PR.Code_ERROR).setMsg('通用删除,删除异常:' + e)

    # 通用新增
    def insert(self):
        _PR = PR.getInstance()
        if self.BO is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用新增，未设置修改对象")
        if self.data is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用新增，未给出参数")
        if self.ds is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用新增，未设置数据源")
        else:
            try:
                insert_bean = Bean().getInsertBean(self.data, self.BO)
                MongoEng(self.ds).getCollection()
                bo = self.BO(**insert_bean)
                bo.save()
                return _PR.setResult(bo).setCode(PR.Code_OK).setMsg('通用查询,查询成功')
            except Exception as e:
                return _PR.setResult(None).setCode(PR.Code_ERROR).setMsg('通用新增,新增异常:' + str(e))

    # 通用更新
    def update(self):
        _PR = PR.getInstance()
        if self.BO is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用更新，未设置修改对象")
        if self.data is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用更新，未给出参数")
        if self.ds is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用更新，未设置数据源")
        else:
            try:
                _id, update_bean = Bean().getUpdateBean(self.data, self.BO, ['_id'])
                MongoEng(self.ds).getCollection()
                res = self.BO.objects(id=_id).update_one(**update_bean)
                if res == 1:
                    return _PR.setResult(self.data).setCode(PR.Code_OK).setMsg('通用更新,更新成功')
                else:
                    return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg('通用更新,更新失败')
            except Exception as e:
                return _PR.setResult(None).setCode(PR.Code_ERROR).setMsg('通用更新,更新异常:' + str(e))

    # 通用查询
    # 不带 filters 返回结果为一条数据，否则返回结果为数组
    # filters = {
    #         'toolCode': data.get('toolCode'),
    #         'toolCodeId': data.get('toolCodeId'),
    #         'toolName__contains': data.get('toolName'),
    #         'toolPort': data.get('toolPort'),
    #         'toolHost': data.get('toolHost'),
    #         'toolUser__contains': data.get('toolUser')
    #     }
    # par = {'pageNum':1,'pageSize':2，'order':'+_id'}
    def search(self, filters=None, par=None, only=[]):
        _PR = PR.getInstance()
        page_num = 1
        page_size = DEFAULT_SEARCH_MAX_SIZE
        order = '+_id'
        if self.BO is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用查询，未设置修改对象")
        if self.data is None and filters is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用查询，未给出参数")
        if self.ds is None:
            return _PR.setResult(self.data).setCode(PR.Code_ERROR).setMsg("通用查询，未设置数据源")
        else:
            if par is not None:
                page_num = par.get('pageNum', 1)
                page_size = par.get('pageSize', DEFAULT_SEARCH_MAX_SIZE)
                order = par.get('order', '+_id')
            try:
                MongoEng(self.ds).getCollection()
                if filters is None:
                    if len(only) > 0:
                        res = self.BO.objects.filter(id=self.data.get('_id')).only(*only).first()
                    else:
                        res = self.BO.objects.filter(id=self.data.get('_id')).first()
                else:
                    f = Q(**Bean().getSearchBean(filters))
                    skip = (page_num - 1) * page_size
                    if len(only) > 0:
                        res = self.BO.objects.filter(f).only(*only)[skip: skip + page_size].order_by(order)
                    else:
                        res = self.BO.objects.filter(f)[skip: skip + page_size].order_by(order)
                return _PR.setCode(PR.Code_OK).setPageNum(page_num).setPageSize(page_size).setResult(res).setMsg('通用查询,查询成功')
            except Exception as e:
                return _PR.setResult(None).setCode(PR.Code_ERROR).setMsg('通用查询,查询异常:%s' % e)


def getInstance(ds=init.ROOT_DB_DS, bo=None, data=None):
    return SingleTableOpt(ds=ds, bo=bo, data=data)
