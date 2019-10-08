#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import init
from bin.base.tool import JsonFileFunc
from bin.base.data import Path
from bin.base.log import Logger
from bin.logic.BO.OAMP.ToolBo import ToolBo
from bin.base.db.MongoEng import MongoEng
from bin.base.sys.Bean import Bean
from mongoengine import Q
import json
from bin.base.sys import PR
from bin.base.sys import SingleTableOpt
from bin.logic.BO.OAMP.CodeBo import CodeBo


class MemoryInit(object):
    def __init__(self):
        pass

    def init_code(self):
        code_info_count = 0
        page_size = 1000
        page_num = 1
        while True:
            x = {
                'isCodeType': False
            }
            code_info_res = SingleTableOpt.getInstance().setBO(CodeBo).search(filters=x, par={'pageSize': page_size, 'pageNum': page_num})
            if code_info_res.getCode() == PR.Code_OK and code_info_res.getData() is not None:
                page_count = code_info_res.getPageCount()
                for code_info in code_info_res.getData():
                    code_info_count += 1
                    data = {code_info.get('codeId'): code_info.get('codeValue')}
                    if init.CODE_INFO.get(code_info.get('code')) is None:
                        init.CODE_INFO.update({code_info.get('code'): data})
                    else:
                        init.CODE_INFO.get(code_info.get('code')).update(data)
                if page_count < page_num * page_size:
                    break
                else:
                    page_num += 1
            else:
                break

    # 初始化内存数据
    def init(self):
        self.init_code()
        pass


def getInstance():
    return MemoryInit()
