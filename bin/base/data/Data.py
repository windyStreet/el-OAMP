#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import uuid
import json
import math


# 获取一个填充数组
def getD4tArr(len=10, default_value=0):
    arr = []
    for i in range(len):
        arr.append(default_value)
    return arr


# 判断数据是否为空
def isNone(data):
    try:
        if data is None:
            return True
        elif len(data) == 0:
            return True
    except Exception as e:
        return False


def classToDict(obj):
    '''把对象(支持单个对象、list、set)转换成字典'''
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict


# 获取一个数据的二进制组成位
# eg : 1    --> [1]
# eg : 2    --> [2]
# eg : 5    --> [1,4]
# eg : 15   --> [1, 2, 4, 8]
# eg : 16   --> [16]
# eg : 167  --> [1, 2, 4, 32, 128]
# eg : 168  --> [8, 32, 128]
def get_bin_add_Datas(dec):
    y = 0
    list_x = []
    for x in bin(int(dec)).split("b")[1][::-1]:
        if x != "0":
            list_x.append(int(math.pow(2, y)))
        y = y + 1
    return list_x


# 获取32位UUID
def getUUID():
    return str(uuid.uuid1()).replace("-", "")


def removeJsonAtrr(data, attrArr):
    res = {}
    for key in data.keys():
        if key in attrArr:
            continue
        else:
            res[key] = data.get(key)
    return res


# json 格式转换为字符串
def json_to_str(json_data):
    if isinstance(json_data, str):
        return json_data
    if json_data is None:
        return ''
    return json.dumps(json_data)


def str_to_json(json_str):
    # dir(json_str)
    if check_json_format(json_str):
        return json.loads(json_str, encoding='utf-8')
    else:
        return None


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param:String
    :return: Boolean
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False
