#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import copy

__author__ = 'windyStreet'
__time__ = '2018年12月18日17:42:22'


class NavigationTreeUntil(object):
    # 用于存储全部节点数据

    def __init__(self, node):
        self.node_id = node.get('node_id', None)
        self.parent_id = node.get('parent_id', None)
        self.router_has_child = False if node.get('router_has_child', 'false') == 'false' else True
        self.router_has_icon = False if node.get('router_has_icon', 'false') == 'false' else True
        self.router_icon_class = node.get('router_icon_class')
        self.router_show_name = node.get('router_show_name')
        self.router_name = node.get('router_name')
        self.router_path = node.get('router_path')
        self.menus = []
        self.__node_list = []
        # self.__node_del_list = []

    # 去除重复元素
    # self.__node_list = [{'node_id':'aaa','node_info':'info0'},{'node_id':'bbb','node_info':'info1'},{'node_id':'aaa','node_info':'info2'}]
    def filter_node(self):
        new_node_list = []
        for item in self.__node_list:
            is_add = True
            for new_item in new_node_list:
                if new_item['node_id'] == item['node_id']:
                    is_add = False
                    break
            if is_add:
                new_node_list.append(item)
        self.__node_list = new_node_list


    def get_filter_node(self):
        return self.__node_list

    # 生成返回结果
    def json(self):
        # 去掉重复的数据
        self.filter_node()
        return self.__package_tree(None)

    def add_node(self, node):
        self.__node_list.append(node)
        return self

    def __package_tree(self, cur_node):
        if cur_node is None:  # 寻找顶级节点
            for node in self.__node_list:
                if node.get('parent_id') is None:
                    return self.__package_tree(cur_node=node)
        else:
            td = NavigationTreeUntil(cur_node).__dict__
            for node in self.__node_list:
                if node.get('parent_id') is not None and node.get('parent_id') == cur_node.get('node_id'):
                    td.get('menus').append(self.__package_tree(cur_node=node))
            return td


def getInstance(node={}):
    return NavigationTreeUntil(node)
