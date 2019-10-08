#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import copy

__author__ = 'windyStreet'
__time__ = '2018年12月18日17:42:22'


class TreeUntil(object):
    # 用于存储全部节点数据

    def __init__(self, node):
        self.id = node.get('node_id', None)
        self.parent_id = node.get('parent_id', None)
        self.label = node.get('label', None)
        self.value = node.get('value', None)
        self.children = []
        self.__node_list = []
        # self.__node_del_list = []

        # 生成返回结果

    def json(self):
        # self.__node_del_list = self.__node_list
        # import time
        # t1 = time.time()
        return self.__package_tree(None)
        # t2 = time.time()
        # print(t2 - t1)
        # return x

    def add_node(self, node):
        item = node
        item['value'] = copy.copy(node)
        self.__node_list.append(item)
        return self

    # def set_top_node(self):

    def __package_tree(self, cur_node):
        # self.__node_list = self.__node_del_list.copy() # 赋值 复制当前循环对象，减少循环次数
        if cur_node is None:  # 寻找顶级节点
            for node in self.__node_list:
                if node.get('parent_id') is None:
                    return self.__package_tree(cur_node=node)
        else:
            # self.__node_del_list.remove(cur_node) # 移除不需要循环的对象
            td = TreeUntil(cur_node).__dict__
            for node in self.__node_list:
                if node.get('parent_id') is not None and node.get('parent_id') == cur_node.get('node_id'):
                    td.get('children').append(self.__package_tree(cur_node=node))
            return td


def getInstance(node={}):
    return TreeUntil(node)
