#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.tool import JsonFileFunc
from bin.base.data import Path

J = JsonFileFunc.getInstance()
P = Path.getInstance()

class ClusterModeInit(object):
    def __init__(self):
        pass

    def init(self):
        pass

def getInstance():
    return ClusterModeInit()