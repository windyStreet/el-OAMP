#!/usr/bin/env python
# !-*- coding:utf-8 -*-


# 对外发布接口
class Outer_services(object):
    def __init__(self):
        pass
    '''
    @author:windyStreet
    @time:2017年8月7日17:38:47
    @version:V0.1.0
    @func:"信息发送"·
    @param:data:{
       "send_type":7,([1:邮件发送,2:微信发送,4:短信发送],7=1+2+4 邮件、微信、短信均发送,default val 1) int
       "sender":{"sender_name":"open-falcon","sender_account":"yaogc@longrise.com.cn"}（able null,default sender_name:运维平台，sender_account:devops@longrise.com.cn）string
       "receivers":["windyStreet","wuqiang"],string[]
       "group_receiver":{
           "group_name":YXYBB",string
           "receive_level":"接收级别"（default 10，默认参数,值越大发送范围越大）int
       }
       "msg":{
           "type":"消息类型", （这个决定信息是进行模板化处理）string
           "title":"信息主题", string
           "content":"信息内容" string
       }
    } json (not null)
    @notice:""
    @PR:{
       "code": code
       "msg":msg
       "result":None
    }
    @return:PR
    '''
    def send_msg(self, data):
        return None
