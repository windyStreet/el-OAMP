#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import sys
import os

__author__ = 'windyStreet'
__time__ = '2017-03-17'
import datetime


class Path(object):
    def __init__(self):
        self.path = sys.path[0]
        self.projectDirPath = self.path[0:self.path.rindex('bin')]
        self.confDirPath = self.projectDirPath + 'conf'
        self.binPath = self.projectDirPath + 'bin'
        self.logsDirPath = self.projectDirPath + 'logs'
        self.scriptsDirPath = self.projectDirPath + 'scripts'
        self.filesDirPath = self.binPath + os.sep+'base'+os.sep+ 'files'
        self.runtimeDirPath = self.projectDirPath + 'runtime'
        self.webPath = self.projectDirPath + 'dist'
        self.databasePath = self.binPath + os.sep + 'utils' + os.sep + 'database'
        pass

    def getRulePath(self, rule=None):
        if rule is None:
            return
        else:
            return str(datetime.datetime.now().strftime(rule))


def getInstance():
    return Path()
