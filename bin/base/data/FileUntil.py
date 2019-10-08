#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import codecs
import os


class FileUntil(object):
    def __init__(self):
        pass

    def createFile(self, path, content):
        try:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with codecs.open(path, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(str(content))
        except Exception as e:
            print("create %s fail ，case by : %s" % (str(path), str(e)))

    def readFile(self, path):
        data = None
        try:
            with open(path, 'r') as tmpFile:
                data = tmpFile.read()
        except Exception as e:
            print("read file [ %s ] not exits : %s" % (str(path), str(e)))
        return data

    def delFile(self, path):
        pass

    def Files(self, path):
        pass

    def get_recursive_dir_files(self, dir_path, endwith=None, all_file=[]):
        file_list = os.listdir(dir_path)
        for filename in file_list:

            file_path = os.path.join(dir_path, filename)
            if os.path.isdir(file_path):
                self.get_recursive_dir_files(file_path, endwith, all_file)
            elif endwith is not None and not filename.endswith(endwith):
                # 未匹配到对应的文件规则 跳过
                continue
            else:
                all_file.append(file_path)
        return all_file

    def get_cur_dir_files(self, dir_path, endwith=None, all_file=[]):
        file_list = os.listdir(dir_path)
        for filename in file_list:
            if filename.endswith(endwith):
                file_path = os.path.join(dir_path, filename)
                if os.path.isdir(file_path):
                    self.get_recursive_dir_files(file_path, all_file)
                else:
                    all_file.append(file_path)
        return all_file

    def get_file_relation_path(self, dir_path):
        res = []
        files = self.get_recursive_dir_files(dir_path=dir_path)
        for file in files:
            res.append(str(file).replace(dir_path, "").replace("\\", "/"))
        return res

    def get_html_file_relation_path(self, dir_path):
        res = []
        files = self.get_recursive_dir_files(dir_path=dir_path,endwith='html')
        for file in files:
            res.append(str(file).replace(dir_path, "").replace("\\", "/"))
        return res


def getInstance():
    return FileUntil()
