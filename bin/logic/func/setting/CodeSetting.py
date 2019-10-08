#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.sys import PR
from bin.base.sys import Msg
from bin.base.sys import SingleTableOpt
from bin.base.tool import RabbitMQ
from bin.logic.BO.OAMP.CodeBo import CodeBo


class CodeSetting(object):
    def __init__(self):
        pass

    # 新增代码表类型信息
    def OAMP_insert_code_type_info(self, data):
        __sessionId__ = data.get('__sessionId__')
        code = data.get('code', None)
        if code is None:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('par error')
        else:
            x = {'code': code, 'isCodeType': True}
            _res = SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x)
            if _res is not None and _res.getCode() == PR.Code_OK and _res.getData() is not None:
                return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('代码表类型已存在')
            else:
                data['isCodeType'] = 1
                _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data).insert()
                if _PR is not None and _PR.getCode() == PR.Code_OK:
                    msg = Msg.getInstance().set_msg('插入[' + code + ']代码表类型数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return _PR

    # 删除代码表类型信息
    def OAMP_delete_code_type_info(self, data):
        __sessionId__ = data.get('__sessionId__')
        isCodeType = data.get('isCodeType', None)
        if isCodeType is None:
            return PR.getInstance().setResult(PR.Code_ERROR).setResult({}).setMsg('删除代码表参数错误')
        elif isCodeType is False:
            return self.OAMP_delete_code_data(data=data)
        else:
            code = data.get('code', None)
            x = {'code': code}
            _res = SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x)
            if _res is not None and _res.getCode() == PR.Code_OK and _res.getPageCount() == 1:
                msg = Msg.getInstance().set_msg('删除[' + code + ']代码表类型数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
                RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).delete()
            else:
                return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('代码表类型下仍存在未删除的代码值')

    # 更新代码表类型信息
    def OAMP_update_code_type_info(self, data):
        __sessionId__ = data.get('__sessionId__')
        # 先查询原始数据
        _org_data = SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).search()
        if _org_data is not None and _org_data.getCode() == PR.Code_OK:
            code = _org_data.getData().get('code', None)
            if code is None:
                return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('代码表源数据异常')
            else:
                # 查询所有code值相同的代码表
                x = {
                    'code': code,
                    'isCodeType': False
                }
                _code_res = SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x)
                if _code_res is not None and _code_res.getCode() == PR.Code_OK and _code_res.getData() is not None:
                    for code_data in _code_res.getData():
                        code_data['__sessionId__'] = __sessionId__
                        code_data['code'] = data.get('code')
                        code_data['codeName'] = data.get('codeName')
                        _update_res = self.OAMP_update_code_data(data=code_data)
                        if _update_res is None or _update_res.getCode() != PR.Code_OK:
                            return _update_res
                _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).update()
                if _PR is not None and _PR.getCode() == PR.Code_OK:
                    msg = Msg.getInstance().set_msg('更新[' + code + ']代码表类型数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
                    RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
                return _PR
        else:
            return PR.getInstance().setCode(PR.Code_ERROR).setResult({}).setMsg('代码表数据不存在')

        # 查询代码表table页面数据

    def OAMP_search_code_info_list(self, data):
        x = {
            'code__contains': data.get('code', ''),
            'codeName__contains': data.get('codeName', ''),
            'isCodeType': True if data.get('onlyShowCodeType') else '',
        }
        return SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x, par=data)

    # 插入代码表值数据
    def OAMP_insert_code_data(self, data):
        __sessionId__ = data.get('__sessionId__')
        _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).insert()
        if _PR is not None and _PR.getCode() == PR.Code_OK:
            msg = Msg.getInstance().set_msg('插入[' + data.get('code') + ']代码表值数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return _PR

    # 删除代码表值数据
    def OAMP_delete_code_data(self, data):
        __sessionId__ = data.get('__sessionId__')
        _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).delete()
        if _PR is not None and _PR.getCode() == PR.Code_OK:
            msg = Msg.getInstance().set_msg('删除[' + data.get('code') + ']代码表值数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return _PR

        # 更新代码表值数据

    def OAMP_update_code_data(self, data):
        __sessionId__ = data.get('__sessionId__')
        _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data=data).update()
        if _PR is not None and _PR.getCode() == PR.Code_OK:
            msg = Msg.getInstance().set_msg('更新[' + data.get('code') + ']代码表值数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
        return _PR

    # 查询代码数据列表【仅查询代码表值】
    def OAMP_search_code_data_list(self, data):
        x = {
            'code': data.get('code'),
            'isCodeType': False
        }
        return SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x)

    ###########################

    # # 通过ID获取信息
    # def _getCodeInfoById(self, data):
    #     _PR = PR.getInstance()
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     res = CodeBo.objects.filter(id=data.get('_id')).first()
    #     return _PR.setResult(res).setCode(PR.Code_OK).setMsg('通过id查询结果')
    #
    # # 通过ID更新
    # def _updateCodeInfoById(self, data):
    #     return SingleTableOpt.getInstance().setData(data).setBO(CodeBo).update()
    #
    # def _deleteCodeInfoById(self, data):
    #     _PR = PR.getInstance()
    #     if data.get('_id') is None:
    #         return _PR.setResult(data).setCode(PR.Code_PARERROR).setMsg('删除code数据时，传递参数缺失')
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     x = {
    #         'id': data.get('_id')
    #     }
    #     f = Q(**Bean().getSearchBean(x))
    #     res = CodeBo.objects.filter(f).delete()
    #     if res == 1:
    #         return _PR.setResult(res).setCode(PR.Code_OK).setMsg('删除code数据成功')
    #     else:
    #         return _PR.setResult(res).setCode(PR.Code_WARNING).setMsg('删除成功,但未找到对应数据')
    #
    # # 插入代码信息[代码值、代码类型]
    # def OAMP_iCodeInfo(self, data):
    #     __sessionId__ = data.get('__sessionId__')
    #     _PR = PR.getInstance()
    #     if data is not None:
    #         isExist = True
    #         # 插入代码表类型信息
    #         if data.get('isCodeType') == 1:
    #             # 先查询是否存在
    #             res = Service_logic.getInstance().OAMP_getCodeTypeInfo(data={'code': data.get('code')})
    #             if res is not None and res.getCode() == PR.Code_OK and res.getResult() is not None:
    #                 r = res.getResult()
    #                 _PR.setResult(r).setCode(PR.Code_WARNING).setMsg("插代码类型数据已存在")
    #             else:
    #                 isExist = False
    #         # 插入代码值信息
    #         else:
    #             res = Service_logic.getInstance().OAMP_getCodeValueInfo(data={'code': data.get('code'), 'codeId': data.get('codeId')})
    #             if res is not None and res.getCode() == PR.Code_OK and res.getResult() is not None:
    #                 r = res.getResult()
    #                 _PR.setResult(r).setCode(PR.Code_WARNING).setMsg("插代码值数据已存在")
    #             else:
    #                 isExist = False
    #         if isExist is False:
    #             _PR = SingleTableOpt.getInstance().setBO(CodeBo).setData(data).insert()
    #             msg = Msg.getInstance().set_msg('插入代码表数据').set_user_name(session_id=__sessionId__).set_type_sys_log().set_par(data).json()
    #             RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
    #     else:
    #         _PR.setResult(data).setCode(PR.Code_PARERROR).setMsg('插入code数据时，传递参数错误')
    #     return _PR
    #
    # # 获取代码表类型信息
    # # data {code:''}
    # def OAMP_getCodeTypeInfo(self, data):
    #     _PR = PR.getInstance()
    #     x = {
    #         'code': data.get('code'),
    #         'isCodeType': True
    #     }
    #     f = Q(**x)
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     res = CodeBo.objects.filter(f).first()
    #     return _PR.setResult(res).setCode(PR.Code_OK).setMsg("查询代码表类型信息数据成功")
    #
    # # 获取具体代码表值信息
    # # data {code:'',codeId:''}
    # def OAMP_getCodeValueInfo(self, data):
    #     _PR = PR.getInstance()
    #     x = {
    #         'code': data.get('code'),
    #         'codeId': data.get('codeId'),
    #         'isCodeType': False
    #     }
    #     f = Q(**x)
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     res = CodeBo.objects.filter(f).first()
    #     return _PR.setResult(res).setCode(PR.Code_OK).setMsg("查询代码表类型信息数据成功")
    #
    # # 获取同类代码表值信息
    # # data {code:''}
    # def OAMP_get_code_value_info_list(self, data):
    #     _PR = PR.getInstance()
    #     x = {
    #         'code': data.get('code', ''),
    #         'isCodeType': False
    #     }
    #     f = Q(**x)
    #     MongoEng(init.ROOT_DB_DS).getCollection()
    #     res = CodeBo.objects.filter(f).all()
    #     return _PR.setResult(res).setCode(PR.Code_OK).setMsg("查询代码表类型信息数据成功")
    #
    # # 更新代码表类型信息
    # def OAMP_delete_code_info(self, data):
    #     _PR = PR.getInstance()
    #     # 获取到原始的代码表类型信息
    #     res = self._getCodeInfoById(data)
    #     if res is not None and res.getCode() == PR.Code_OK and res.getResult() is not None:
    #         item = res.getData()
    #         o_code = item.get('code')
    #         # 获取同类代码表值信息
    #         res_1 = Service_logic.getInstance().OAMP_get_code_value_info_list(data={'code': o_code})
    #         if res_1 is not None and res_1.getCode() == PR.Code_OK and res_1.getResult() is not None and res_1.getData() is not None:
    #             for codeValueInfo in res_1.getData():
    #                 codeValueInfo['code'] = data.get('code')
    #                 codeValueInfo['codeName'] = data.get('codeName')
    #                 res_2 = self._updateCodeInfoById(data=codeValueInfo)
    #                 if res_2 is not None and res_2.getCode() == PR.Code_OK and res_2.getResult() is not None:
    #                     pass
    #                 else:
    #                     return _PR.setResult(codeValueInfo).setCode(PR.Code_ERROR).setMsg('更新代码值数据失败')
    #         _id, updateBean = Bean().getUpdateBean(data, CodeBo, [])
    #         res_3 = self._updateCodeInfoById(data)
    #         if res_3 is not None and res_3.getCode() == PR.Code_OK and res_3.getResult() is not None:
    #             return _PR.setResult(updateBean).setCode(PR.Code_OK).setMsg('更新代码类型数据成功')
    #         else:
    #             return _PR.setResult(updateBean).setCode(PR.Code_ERROR).setMsg('更新代码类型数据失败')
    #     else:
    #         return _PR.setResult(data).setCode(PR.Code_PARERROR).setMsg('待修改的代码类型已不存在')
    #
    # # 更新代码值数据
    # def OAMP_uCodeValueInfo(self, data):
    #     return self._updateCodeInfoById(data=data)
    #
    # # 检查代码表中是否还存在代码值
    # def _checkIsHasCodeValue(self, data):
    #     res = Service_logic.getInstance().OAMP_get_code_value_info_list(data)
    #     if res is not None and res.getCode() == PR.Code_OK and res.getResult() is not None and res.getData() is not None and len(res.getData()) > 0:
    #         return True
    #     else:
    #         return False
    #
    # # 删除代码表信息
    # def OAMP_dCodeInfo(self, data):
    #     if data.get('isCodeType') == 1 or data.get('isCodeType') is True:
    #         if self._checkIsHasCodeValue(data):
    #             return PR.getInstance().setResult(None).setCode(PR.Code_WARNING).setMsg('该代码表存在代码值未删除')
    #         else:
    #             return self._deleteCodeInfoById(data=data)
    #     else:
    #         return self._deleteCodeInfoById(data=data)


def getInstance():
    return CodeSetting()
