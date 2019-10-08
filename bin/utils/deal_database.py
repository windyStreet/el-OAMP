#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.tool import JsonFileFunc
from bin.base.data import FileUntil, Path
import json
import os

P = Path.getInstance()
F = FileUntil.getInstance()
J = JsonFileFunc.getInstance()


class deal_database(object):
    def __init__(self):
        pass

    def read_database(self):
        # 读取数据表
        database_path = P.databasePath
        # files = F.get_cur_dir_files_endwith(dir_path=database_path, endwith=".json")
        files = F.get_recursive_dir_files(dir_path=database_path, endwith=".json")
        base_file = None
        files_to_p = []
        for f in files:
            if str(f).endswith('base.json'):
                base_file = f
            else:
                files_to_p.append(f)
        return base_file, files_to_p

    def get_content_json(self, b_f, to_f):
        jo = {}
        j = J.readFile(b_f)
        j_1 = J.readFile(to_f)
        jo.update(j)
        jo.update(j_1)
        return jo

    def create_py_file(self, content, class_name, py_path):
        # 生成py 文件
        str_content_header = '''
#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime
from bin.base import DBCODE
from bin.base import Data
'''
        str_switch = '\r\n'
        str_format = '\'\'\''
        str_content = str_content_header + str_switch
        str_content += str_format
        str_content += str_switch
        str_content += json.dumps(content, sort_keys=True, indent=4, ensure_ascii=False)
        str_content += str_format
        str_content += str_switch
        str_content += 'class ' + class_name + '(object):' + str_switch
        str_content += '    def __init__(self):' + str_switch

        # '''
        #     def __init__(self):
        #         self._id = None
        #         self.createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        #         self.updateTime = None
        #         self.project_name = None
        #         self.statistic_type = None
        #         self.statistic_name = None
        # '''
        #

        for k in sorted(content.keys()):
            s = ''
            if k == 'createTime':
                s = '        self.createTime = datetime.datetime.now().strftime(\'%Y-%m-%d %H:%M:%S.%f\')'
            # elif k == 'table':
            #     s = '        self.table = \'' + content.get(k) + '\''
            else:
                s = '        self.' + k + ' = None'
            str_content += s + str_switch
        str_content += str_switch
        # ---- json 定义--
        str_content += '    @property' + str_switch
        str_content += '    def json(self):' + str_switch
        str_content += '        """JSON format data."""' + str_switch
        str_content += '        json = {}' + str_switch
        for k in sorted(content.keys()):
            str_content += '        if self.' + k + ' is not None:' + str_switch
            str_content += '            json[\'' + k + '\'] = self.' + k + '' + str_switch
            if k == '_id':
                str_content += '        else:' + str_switch
                str_content += '            json[\''+k+'\'] = Data.getUUID()' + str_switch

        str_content += '        return json' + str_switch
        str_content += str_switch
        # --update json 定义
        str_content += '    @property' + str_switch
        str_content += '    def update_json(self):' + str_switch
        str_content += '        """JSON format data."""' + str_switch
        str_content += '        update_json = {DBCODE.RELATION_UPDATE: self.json}' + str_switch
        str_content += '        return update_json' + str_switch
        str_content += str_switch

        # -- get set 方法定义
        for k in sorted(content.keys()):
            k1 = str(k)[0].upper()+str(k)[1:]
            s = '    def set' + k1 + '(self, ' + k + '):' + str_switch
            s += '        self.' + k + ' = ' + k + str_switch
            s += '        return self' + str_switch
            s += str_switch
            s += '    def get' + k1 + '(self):' + str_switch
            s += '        return self.' + k + str_switch
            s += str_switch
            str_content += s
        str_content += 'def getInstance():' + str_switch
        str_content += '    return ' + class_name + '()'
        F.createFile(path=py_path, content=str_content)


if __name__ == '__main__':
    ob = deal_database()
    base_file, files_to_p = ob.read_database()
    for file_to_p in files_to_p:
        content = ob.get_content_json(base_file, file_to_p)
        file_name = os.path.basename(file_to_p)
        cur_p = str(file_to_p).split(os.sep)[-2]
        class_name = file_name.split('.')[0].capitalize() + 'BO'
        py_path = P.binPath + os.sep + 'logic' + os.sep + 'BO' + os.sep + cur_p + os.sep + class_name + '.py'
        ob.create_py_file(content=content, class_name=class_name, py_path=py_path)
