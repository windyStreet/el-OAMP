#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import os


class Falcon_mail_data(object):
    def __init__(self, data):
        self.receivers = data.get('tos')
        self.header = data.get("subject")
        self.content = data.get("content")
        self.content_map = {
            "Endpoint": "机器节点",
            "Timestamp": "报警时间",
            "Metric": "采集项",
            "Tags": "标签",
            "all(#1)": "阈值",
            "Note": "注释",
            "Max": "最大次数",
            "Current": "当前次数",
            "URL": "模板链接"
        }

    def deal_header(self):
        _list = str(self.header[0]).replace("]", " ").replace("[", " ").split()
        p = ''
        for i in _list:
            if i.find("all") != -1:
                p = _list.index(i)
            else:
                pass
        metric = _list[p + 1]
        res = ''
        if _list[1] == "PROBLEM":
            res = res + "★故障发生"
            res = res + "【" + _list[2] + "】"
            res = res + "机器检测到" + "【" + metric + "】" + "【" + _list[6] + "】"
            res = res + _list[-2] + ' ' + _list[-1]
        else:
            res = res + "☆故障解除"
            res = res + "【" + _list[2] + "】"
            res = res + "机器检测到" + "【" + metric + "】" + "【" + _list[6] + "】"
            res = res + _list[-2] + ' ' + _list[-1]
        return res

    def deal_content(self):
        return self.content[0]
        str_s = str(self.content[0].split('\r\n')).replace("'", "").strip("]").strip("[").split(",")
        result = []
        for s in str_s:
            s = s.strip(" ")
            result.append(s)

        res = "<table border='1'> "
        res = str(res) + "<tr>"
        res = str(res) + "<td style='min-width: 150px;'>" + "运行状态" + "</td>"
        res = str(res) + "<td style='min-width: 600px;'>" + str(result[0]).strip(" ") + "</td>"
        res = str(res) + "</tr>"

        res = str(res) + "<tr>"
        res = str(res) + "<td>" + "发生次数" + "</td>"
        res = str(res) + "<td >" + str(result[1]).strip(" ") + "</td>"
        res = str(res) + "</tr>"
        for i in range(2, 9):
            res = str(res) + "<tr>"
            res = str(res) + "<td>" + self.content_map.get(str(result[i]).split(":")[0], str(result[i]).split(":")[0]) + "</td>"
            res = str(res) + "<td >" + str(result[i]).split(":")[1].strip(" ") + "</td>"
            res = str(res) + "</tr>"

        res = str(res) + "<tr>"
        res = str(res) + "<td>" + "报警时间" + "</td>"
        res = str(res) + "<td>" + str(result[9][10:]) + "</td>"
        res = str(res) + "</tr>"

        res = str(res) + "<tr>"
        res = str(res) + "<td>" + "模板链接" + "</td>"
        res = str(res) + "<td><a href='#'>" + str(result[10]).strip(" ") + "</a></td>"
        res = str(res) + "</tr>"
        res = str(res) + "</table>"
        return res

    def deal_data(self):
        return self.receivers, self.deal_header(), self.deal_content()


def getInstance(data):
    return Falcon_mail_data(data=data)
