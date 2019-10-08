#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.data import Data, Time
from bin.base.sys.Session import SessionDataOpt


class Bean(object):
    def getSearchBean(self, data):
        if data is not None:
            res = {}
            for k, v in data.items():
                if k is not None and k != '' and v != '' and v is not None:
                    res[k] = v
            return res
        return None

    def getInsertBean(self, data, classBo=None, attrArr=None):
        if classBo is None:
            return None
        _insertBean = {}
        for key in classBo._fields:
            _insertBean[key] = data.get(key)
        _insertBean['id'] = data.get('_id', Data.getUUID())
        _insertBean['createTime'] = Time.get_create_time()
        _insertBean['creator'] = SessionDataOpt(sessionId=data.get('__sessionId__', 'super')).getSessionData('userName')
        return _insertBean

    def getUpdateBean(self, data, classBo=None, attrArr=None):
        if classBo is None:
            return None
        _updateBean = {}
        for key in classBo._fields:
            _updateBean[key] = data.get(key)
        _updateBean['id'] = data.get('_id')
        _updateBean['updateTime'] = Time.get_update_time()
        _updateBean['updater'] = SessionDataOpt(sessionId=data.get('__sessionId__', 'super')).getSessionData('userName')
        return _updateBean.get('id'), Data.removeJsonAtrr(_updateBean, attrArr)
