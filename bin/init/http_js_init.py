#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import os

from bin import init
from bin.base.data import FileUntil, Path

tmp = '''//异步请求获取数据
function asyncRequest(method,data, callback,callback2) {
    reqData={
        "method":method,
        "data":data
    }
    reqData=JSON.stringify(reqData)
    $.ajax({
        headers: {
            Accept:"application/json; charset=utf-8"
        },
        type: "post",
        url: "/context/service",
        data: reqData,
        dataType: "json",
        async:"true",
        success: function (res) {
            //var result = JSON.parse(res);
            callback(res);
        },
        failure:function (res) {
            callback2(res)
        },
    });
}'''


def rewrite_http_js():
    context = init.CONF_INFO.get("server", {"context": ""}).get("context")
    content = tmp.replace("context", context)
    path = Path.getInstance().webPath + os.sep + "js" + os.sep + 'http.js'
    FileUntil.getInstance().createFile(path=path, content=content)


rewrite_http_js()
