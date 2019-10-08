from bin.base.data import Time
from bin import init
from bin.base.sys.Session import SessionDataOpt
from bin.base.tool import RabbitMQ
from bin.logic.func.record import ExecFuncRecord
from bin.base.data import Data
from bin.base.log import Logger

L = Logger.getInstance()


class PublishMQFunc(object):
    def __init__(self):
        self.project = init.CONTEXT
        self.method = None
        self.par = None
        self.msg = '描述'
        self.user_name = 'sys'
        self.exec_count = 0
        self.createTime = Time.get_create_time()  # '创建时间'

    def json(self):
        json = {
            'project': self.project,
            'method': self.method,
            'par': Data.json_to_str(self.par),
            'user_name': self.user_name,
            'creteTime': self.createTime,
            'exec_count': self.exec_count,
            'msg': self.msg,


        }
        return json

    def set_project(self, project):
        self.project = project
        return self

    def set_method(self, method):
        self.method = method
        return self

    def set_par(self, par):
        self.par = par
        return self

    def set_user_name(self, user_name=None, session_id=None):
        if user_name is not None:
            self.user_name = user_name
            return self
        if session_id is not None:
            self.user_name = SessionDataOpt(sessionId=session_id).getUserName()
        return self

    def set_exec_count(self, exec_count):
        self.exec_count = exec_count
        return self

    def add_exec_count(self, exec_count):
        self.exec_count = exec_count + 1
        return self

    def publish(self):
        # 记录进入数据库中 , 一次点击记录超过三次执行，放弃该事件
        if self.exec_count <= 3:
            ExecFuncRecord.getInstance().record(data=self.json()) # 记录执行事件
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_EXEC, msg=self.json())
        else:
            L.error('%s项目%s功能任务执行超过三次，放弃发布该任务' % (str(self.project), str(self.method)))


def getInstance():
    return PublishMQFunc()
