#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import PR

import os


class ProjectUpdate(object):
    def __init__(self):
        pass

    def get_path_info(self, path, is_show_file):
        if not os.path.isdir(path):
            return []
        res = []
        # for root, dirs, files in os.walk(path, topdown=False):
        dirs = sorted(os.listdir(path))
        for d in dirs:
            tmp_path = os.path.join(path, d)
            if is_show_file == '1' and os.path.isfile(tmp_path):
                res.append({'res_name': d, 'resource_type_code_id': '2', 'res_path': tmp_path})
            elif is_show_file == '0' and os.path.isdir(tmp_path):
                res.append({'res_name': d, 'resource_type_code_id': '1', 'res_path': tmp_path})
        return res

    # 获取lib资源信息
    def OAMP_get_lib_res_info(self, data):
        path = data.get('path')
        is_show_file = data.get('isShowFile', '1')
        path = path + os.sep + 'lib'
        res = self.get_path_info(path, is_show_file)
        return PR.getInstance().setCode(PR.Code_OK).setResult({'data': res}).setMsg('查询客户端资源文件信息成功')

    # 获取ResourceLib资源信息
    def OAMP_get_ResourceLib_res_info(self, data):
        path = data.get('path')
        is_show_file = data.get('isShowFile', '1')
        path = path + os.sep + 'ResourceLib'
        res = self.get_path_info(path, is_show_file)
        return PR.getInstance().setCode(PR.Code_OK).setResult({'data': res}).setMsg('查询客户端资源文件信息成功')

    # 获取static资源信息
    def OAMP_get_static_res_info(self, data):
        path = data.get('path')
        is_show_file = data.get('isShowFile', '1')
        res = self.get_path_info(path, is_show_file)
        return PR.getInstance().setCode(PR.Code_OK).setResult({'data': res}).setMsg('查询客户端资源文件信息成功')


def getInstance():
    return ProjectUpdate()
