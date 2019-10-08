#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import PR
from bin.base.data import Data
from bin.base.data.ResultThread import ResultThread
import requests
from bin.base.log import Logger

L = Logger.getInstance('PostUntil.log')


class PostUntil(ResultThread):
    def pr_post(self, url, par=None, json_par=None, time_out=3, except_res=None, request_ip=None):
        _PR = PR.getInstance()
        L.debug('请求地址为:%s , 请求参数为:[json]%s | [str]%s  , 请求ip为:%s' % (str(url), str(json_par), str(par), str(request_ip)))
        try:
            if json_par is not None:
                resp = requests.post(url=url, json=json_par, timeout=time_out)
            else:
                resp = requests.post(url=url, data=par, timeout=time_out)
            if resp.status_code == 200 and (except_res is None or (except_res is not None and str(resp.text) == str(except_res))):
                re_data = Data.str_to_json(str(resp.content, encoding='utf-8'))
                if re_data is not None and re_data.get('result') is not None and re_data.get('result').get('data') is not None:
                    result = re_data.get('result').get('data')
                    result['request_ip'] = request_ip
                    self.res_queue.put(_PR)
                    return _PR.setCode(PR.Code_OK).setData(result).setMsg(re_data.get('msg'))
                else:
                    L.error('PostUntil PR 返回结果解析异常，请检查接口返回值')
                    return PR.getInstance().setCode(PR.Code_ERROR).setData({'request_ip': request_ip}).setMsg('PostUntil PR 返回结果解析异常，请检查接口返回值')
            else:
                self.res_queue.put(_PR)
                L.error('请求返回状态错误,状态码为:%s' % str(resp.status_code))
                return _PR.setCode(PR.Code_REQUESTSTATEERROR).setData({'request_ip': request_ip}).setMsg('请求返回状态错误,状态码为:%s' % str(resp.status_code))
        except Exception as e:
            self.res_queue.put(_PR)
            L.exception('调用PR接口，过程异常:%s' % str(e))
            return _PR.setCode(PR.Code_EXCEPTION).setData({'request_ip': request_ip}).setMsg('调用PR接口，过程异常:%s' % str(e))

    def str_post(self, url, par=None, json_par=None, time_out=3, except_res=None):
        _PR = PR.getInstance()
        try:
            if json_par is not None:
                resp = requests.post(url=url, json=json_par, timeout=time_out)
            else:
                resp = requests.post(url=url, data=par, timeout=time_out)
            if resp.status_code == 200 and (except_res is None or (except_res is not None and str(resp.text) == str(except_res))):
                self.res_queue.put(_PR)
                return _PR.setCode(PR.Code_OK).setResult(str(resp.content)).setMsg('请求成功')
            else:
                self.res_queue.put(_PR)
                return _PR.setCode(PR.Code_REQUESTSTATEERROR).setResult(None).setMsg('请求返回状态错误,状态码为:%s' % str(resp.status_code))
        except Exception as e:
            self.res_queue.put(_PR)
            return _PR.setCode(PR.Code_EXCEPTION).setResult(None).setMsg('调用PR接口，过程异常:%s' % str(e))


def getInstance():
    return PostUntil()
