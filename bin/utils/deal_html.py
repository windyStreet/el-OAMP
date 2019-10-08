#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os, re
from bin.base.data import Path

htmlPath = Path.getInstance().webPath + os.sep

def readFile(filePath):
    newContent = ""
    regAll = []
    with open(filePath, 'r',encoding='utf-8') as f:
        fileContent = f.readlines()
    regs = r'href=\"(.*\.png)\"'
    regAll.append(regs)
    regs = r'href=\"(.*\.css)\"'
    regAll.append(regs)
    regs = r'src=\"(.*\.js)\"'
    regAll.append(regs)
    reg3 = r'^http'
    regs = r'href=\"(.*\.ico)\"'
    regAll.append(regs)
    regs = r'href=\"(.*\.jpg)\"'
    regAll.append(regs)
    regs = r'src=\"(.*\.jpg)\"'
    regAll.append(regs)
    for s in fileContent:
        count = 0
        for ss in regAll:
            regFlag = re.findall(ss, s)
            if len(regFlag) > 0:
                regHttp = re.findall(reg3, regFlag[0])
                if len(regHttp) == 0:
                    newContent += s.replace(regFlag[0], "{{ static_url(\'" + regFlag[0] + "\') }}")
                    count = 0
                    break
                else:
                    count += 1
            else:
                count += 1
        if count != 0:
            newContent += s
    return newContent


def writeFile(filePath, content):
    with open(filePath, 'w',encoding='utf-8') as f:
        f.write(content)


def listFile(filePath):
    for fileName in os.listdir(filePath):
        realPath = filePath + fileName
        if os.path.isfile(realPath):
            content = readFile(realPath)
            writeFile(realPath, content)


listFile(htmlPath)
