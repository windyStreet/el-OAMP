#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.tool import RabbitMQ
from pymongo import MongoClient
from bin import init

if __name__ == '__main__':
    conn = MongoClient('211.154.149.99', 27017)
    db = conn.BBT_TrainRecord
    record_set = db.processRecord
    ds = {
        "toolUser": "longrise",
        # "toolPassword": "longrise",
        # "toolHost": "192.168.7.219",
        "toolPort": 5672,
        "toolName": "",
        'toolHost': '211.154.149.99',
        'toolPassword': 'uCSXBwi7KJfKIx4x',
    }
    init.CONF_INFO = {
        'study_recover': ds
    }
    RM = RabbitMQ.getInstance(ds='study_recover')
    start = 0
    end = 5000000
    limit = 1000
    n = 0
    while (True):
        offset = start + limit * n
        if offset >= end:
            break
        for re_dict in record_set.find({"studyend": {"$gt": "2019-06-13 10:00:00.000", '$lt': "2019-06-14 10:00:00"}, "isvideopass": "1"}).sort('createtime').skip(offset).limit(limit):
            re = {
                'id': re_dict.get("recordid"),
                'cwid': re_dict.get('cwid'),
                'cardno': re_dict.get('cardno'),
                'studentno': re_dict.get('studentno'),
                'effecttime': '1',
                'stuclientip': re_dict.get('ip'),
                'stuclientmacinfo': "BBAPP_MQ_" + re_dict.get('comfrom2'),

            }
            RM.sendMsg(queue='APP_onlineUpdate', msg=re)
        print(offset)
        n = n + 1
