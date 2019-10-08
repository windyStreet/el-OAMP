#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from bin.base.sys.Session import SessionHandler
from bin.base.data import Data


# class BaseWebsocketHandler(tornado.websocket.WebSocketHandler):
#     def get_current_user(self):
#         current_user = self.get_secure_cookie("ID")
#         if current_user:
#             return current_user
#         return None


class MessageWSHandler(WebSocketHandler):
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
        for u in self.users:
            if u.cookies.get('__sessionId__').value == self.cookies.get('__sessionId__').value:  # 相同的cookies
                continue
            u.write_message("{}进入！".format(id(self)))
        MessageWSHandler.users.add(self)  # self是user的实例

    # 发送消息
    def on_message(self, message):
        self.show_message(message)

    # 关闭连接
    def on_close(self):
        if self in MessageWSHandler.users:
            for u in self.users:
                if u == self:
                    continue
                msg = "{}退出！".format(id(self))
                u.write_message(msg)
            MessageWSHandler.users.remove(self)
