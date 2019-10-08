#!/usr/bin/env python
# !-*- coding:utf-8 -*-


'''
{
    "name": "flare",
    "children": [
        {
            "name": "data",
            "children": [
                {
                    "name": "converters",
                    "children": [
                        {"name": "Converters", "value": 721},
                        {"name": "DelimitedTextConverter", "value": 4294},
                        {"name": "GraphMLConverter", "value": 9800},
                        {"name": "IDataConverter", "value": 1314},
                        {"name": "JSONConverter", "value": 2220}
                    ]
                },
                {"name": "DataField", "value": 1759},
                {"name": "DataUtil", "value": 3322}
            ]
        },
        {
            "name": "display",
            "children": [
                {"name": "DirtySprite", "value": 8833},
                {"name": "LineSprite", "value": 1732},
                {"name": "RectSprite", "value": 3623},
                {"name": "TextSprite", "value": 10066}
            ]
        }
    ]
}
'''


class TreeData(object):
    def __init__(self, node):
        self.id = node.get('id', None)
        self.pid = node.get('pid', None)
        self.name = node.get('name', None)
        self.value = node.get('value', None)
        self.node_info_list = []  # 用于存储全部节点数据

    # 生成返回结果
    def json(self):
        return self.__package_tree(None, self.node_info_list)

    # 构建树结构
    def __package_tree(self, parent_node=None, node_list=[]):
        cur_node = parent_node
        if parent_node is None:  # 寻找顶级节点
            for node in node_list:
                if node.get('pid') is None:
                    return self.__package_tree(parent_node=node, node_list=self.node_info_list)
        else:
            td = TreeData(cur_node).__dict__
            for node in node_list:
                if node.get('pid') is not None and node.get('pid') == cur_node.get('id'):
                    td.get('children').append(self.__package_tree(parent_node=node, node_list=node_list))
            return td

    # 单独设置值
    def set_node_data(self, id, pid, name, value):
        self.node_info_list.append({'id': id, 'pid': pid, 'name': name, 'value': value})
        return self

    # 将结果集传入
    def set_node_data_list(self, res):
        for r in res:
            self.set_node_data(id=r.get('_id'), pid=r.get('pid'), name=r.get('name'), value=r.get('value'))
        return self


def getInstance(node={}):
    return TreeData(node=node)

# if __name__ == "__main__":
#     Tree = TreeData({}).set_node_data(id='0', pid=None, name='0', value='0')
#     Tree.set_node_data(id='1', name='1', value='1', pid='0')
#     Tree.set_node_data(id='2', name='2', value='2', pid='0')
#     Tree.set_node_data(id='3', name='3', value='3', pid='0')
#     Tree.set_node_data(id='1.1', name='1.1', value='1.1', pid='1')
#     Tree.set_node_data(id='1.2', name='1.2', value='1.2', pid='1')
#     Tree.set_node_data(id='1.3', name='1.3', value='1.3', pid='1')
#     Tree.set_node_data(id='1.4', name='1.4', value='1.4', pid='1')
#     Tree.set_node_data(id='1.2.1', name='1.2.1', value='1.2.1', pid='1.2')
#     Tree.set_node_data(id='1.2.2', name='1.2.2', value='1.2.2', pid='1.2')
#     Tree.set_node_data(id='1.2.3', name='1.2.3', value='1.2.3', pid='1.2')
#     Tree.set_node_data(id='3.1', name='3.1', value='3.1', pid='3')
#     Tree.set_node_data(id='3.2', name='3.2', value='3.2', pid='3')
#     Tree.set_node_data(id='3.3', name='3.3', value='3.3', pid='3')
#     Tree.json()
#     pass
