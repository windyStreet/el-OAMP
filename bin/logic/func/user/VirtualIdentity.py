from collections import defaultdict
from collections import namedtuple
import random
import datetime
from bin.base.sys import PR
from bin.base.data import Path
import os
from bin.logic.func.user import Identity
from bin.logic.func.user import NameTool
from bin.logic.func.user import NumTool
from bin.logic.func.user import MailTool

NT = NameTool.getInstance()
NUT = NumTool.getInstance()
MAT = MailTool.getInstance()


class VirtualIdentity(object):
    def __init__(self):
        pass

    # 创建虚拟用户
    def OAMP_create_virtual_identity(self, data):
        bron_range_start = data.get('bron_range')[0][:10] if data.get('bron_range') is not None and len(data.get('bron_range')) >= 1 else None
        bron_range_end = data.get('bron_range')[1][:10] if data.get('bron_range') is not None and len(data.get('bron_range')) >= 1 else None
        start_mobile = data.get('start_mobile', None)
        user_list = []
        for i in range(19):
            sex = random.randint(0, 1) if data.get('sex') is None or data.get('sex') == '' else int(data.get('sex'))
            idn = Identity.getInstance()
            cardno = idn.generate_id(sex=sex, bron_range_start=bron_range_start, bron_range_end=bron_range_end)
            idn = Identity.getInstance(id_number=cardno)
            name = NT.gen_name()
            user_info = {
                'cardno': cardno,
                'age': idn.get_age(),
                'sex_code_id': str(idn.get_sex()),
                'bron_date': idn.get_birthday(),
                'area_name': idn.get_area_name(),
                'area_id': idn.get_area_id(),
                'name': name,
                'mobile': NUT.gen_phone_num(start_mobile=start_mobile),
                'address': '',
                'email': MAT.gen_mail(name=name),
                'qq': NUT.gen_QQ(),
                'nickname': NT.gen_nick_name()
            }
            user_list.append(user_info)
        return PR.getInstance().setCode(PR.Code_OK).setMsg('生成身份信息成功').setData(user_list)


def getInstance():
    return VirtualIdentity()
