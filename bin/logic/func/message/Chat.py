#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from tornado.websocket import WebSocketHandler
from bin.base.data import Data
from bin.base.tool import Redis
from bin import init

R_chat = Redis.getInstance(ds=init.ROOT_REDIS_DS, db=init.DEFAULT_CHAT_REDIS_DB)
R_session = Redis.getInstance(ds=init.ROOT_REDIS_DS, db=init.DEFAULT_SESSION_REDIS_DB)


class ChatHandler(WebSocketHandler):
    users = set()

    # 解决跨域问题
    def check_origin(self, origin):
        return True

    # 发送消息给所有人
    def show_message(self, message):
        message_json = Data.str_to_json(message)
        chatMode = message_json.get('chatMode')
        chatId = message_json.get('chatId')
        senderId = message_json.get('senderId')
        print(senderId)
        print(senderId)
        print(senderId)
        msg = message_json.get('msg')

        print(message)
        # x = getGroupConn(connMode,chatId) # 通过链接迷失
        msg = {
            'chatId': chatId,
            'senderId': senderId,
            'msg': msg
        }
        for u in self.users:
            u.write_message(msg)

    # 开启连接
    def open(self, *args, **kwargs):
        # 用户进入，先确定用户的信息
        # 获取用户聊天组id
        # 获取用户
        senderId = self.cookies.get('__sessionId__').value
        R_chat.setJson(senderId, self, 30)
        x = R_chat.getJson(senderId)
        for u in self.users:
            if u.cookies.get('__sessionId__').value == self.cookies.get('__sessionId__').value:  # 相同的cookies
                continue
            u.write_message("{}进入！".format(id(self)))
        ChatHandler.users.add(self)  # self是user的实例

    # 发送消息
    def on_message(self, message):
        self.show_message(message)

    # 关闭连接
    def on_close(self):
        if self in ChatHandler.users:
            for u in self.users:
                if u == self:
                    continue
                msg = "{}退出！".format(id(self))
                u.write_message(msg)
            ChatHandler.users.remove(self)
