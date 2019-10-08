#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import json
import codecs


class JsonFileFunc(object):
    def __init__(self):
        pass

    # read content
    def readFile(self, filePath):
        jsonData = None
        try:
            with open(filePath, 'r', encoding='utf-8') as tmpFile:
                jsonData = json.load(tmpFile)
        except Exception as e:
            print("read [  %s ] not exists, %s", str(filePath),str(e))
        return jsonData

    # create json File
    def createFile(self, filePath, data):
        try:
            with codecs.open(filePath, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            print('create %s fail , %s', str(filePath),str(e))

def getInstance():
    return JsonFileFunc()
