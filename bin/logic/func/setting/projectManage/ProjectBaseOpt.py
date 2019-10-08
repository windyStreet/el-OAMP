#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
from bin.base.log import Logger

L = Logger.getInstance()


class ProjectBaseOpt(object):
    def __init__(self):
        pass

    # 压缩资源
    def __tar_resource(self, tar_home_path, project_opt_version):
        try:
            cmd_str = 'cd %s &&  tar -zcvf %s.tar.gz ./%s' % (tar_home_path, str(project_opt_version), str(project_opt_version))
            L.debug('执行命令:%s' % cmd_str)
            os.system(cmd_str)
            return True
        except Exception as e:
            L.exception('执行压缩资源命令异常:%s' % str(e))
            return False

    # 上传tar包
    # (tar_home_path, tar_name, self.update_server_ip, self.update_share_bak_path)
    def upload_resource(self, tar_home_path, tar_name, upload_server_ip, upload_server_port, upload_store_path):
        try:
            cmd_str = 'cd %s &&  scp -P %s %s root@%s:%s ' % (tar_home_path, str(upload_server_port), str(tar_name), str(upload_server_ip), str(upload_store_path))
            L.debug('执行命令:%s' % cmd_str)
            os.system(cmd_str)
            # return os.popen(cmd_str) is 0
            return True
        except Exception as e:
            L.exception('执行上传命令异常:%s' % str(e))
            return False

    # 标记项目
    def remark_project(self, project_context, project_opt_version, project_opt_last_version, libRes, resourceLibRes, staticFileRes, remark_bak_path, update_ex_resource):
        try:
            replace_info = []
            tar_home_path = remark_bak_path + os.sep + project_context
            remark_home_path = tar_home_path + os.sep + str(project_opt_version)
            remark_lib_home_path = remark_home_path + os.sep + 'lib'
            remark_ResourceLib_home_path = remark_home_path + os.sep + 'ResourceLib'
            if not os.path.exists(remark_lib_home_path):
                os.makedirs(remark_lib_home_path)
            if not os.path.exists(remark_ResourceLib_home_path):
                os.makedirs(remark_ResourceLib_home_path)
            if isinstance(project_opt_version, int):
                # 全量标记
                for update_ex_res in update_ex_resource:
                    for k, re in update_ex_res.items():
                        if k == 'libRes':
                            res_path = remark_lib_home_path
                        elif k == 'ResourceLibRes':
                            res_path = remark_ResourceLib_home_path
                        elif k == 'staticFileRes':
                            res_path = remark_home_path
                        else:
                            return False
                        for r in re:
                            item = {
                                'origin_path': r.get('res_path'),
                                'new_path': res_path
                            }
                            replace_info.append(item)
            else:
                # 增量标记
                item = {
                    'origin_path': remark_bak_path + os.sep + project_context + os.sep + str(project_opt_last_version) + os.sep + '*',
                    'new_path': remark_home_path,
                }
                replace_info.append(item)

            for lib_data in libRes:
                item = {
                    'origin_path': lib_data.get('res_path'),
                    'new_path': remark_lib_home_path,
                }
                replace_info.append(item)

            for resourceLib_data in resourceLibRes:
                item = {
                    'origin_path': resourceLib_data.get('res_path'),
                    'new_path': remark_ResourceLib_home_path,
                }
                replace_info.append(item)

            for staticFile_data in staticFileRes:
                item = {
                    'origin_path': staticFile_data.get('res_path'),
                    'new_path': remark_home_path,
                }
                replace_info.append(item)

            for item in replace_info:
                cmd_str = '\cp -rf %s %s' % (item.get('origin_path'), item.get('new_path'))
                L.debug('执行命令:%s' % cmd_str)
                os.system(cmd_str)
            return self.__tar_resource(tar_home_path, project_opt_version)
        except Exception as e:
            L.exception('标记项目处理过程异常:%s' % str(e))
            return False


def getInstance():
    return ProjectBaseOpt()
