# code 2018年6月7日11:29:59
SCHEDULERS = {}
APS_TASKS = {
    'PROJECT_OPT': 'ApsProjectOptTask',
    'SERVICE_CHECK': 'ApsServiceCheckTask',
}
# 配置文件信息
DEFAULT_SESSION_EXPIRE_TIME = 30 * 60
DEFAULT_SESSION_REDIS_DB = 13
DEFAULT_CHAT_REDIS_DB = 10
DEFAULT_SERVICE_CHECK_REDIS_DB = 12
FILE_UPLOAD_REDIS_DB = 11
# MQ 基础配置
MQ_TIME_OUT = 30
MQ_UPLOAD_TIME_OUT = 60 * 60 * 2  # 上传超时2H

# MQ_QUEUE 队列
MQ_QUEUE_UPLOAD = 'QUEUE_UPLOAD'  # 上传任务
MQ_QUEUE_PROJECT_SERVICE = 'QUEUE_PROJECT_SERVICE'  # 项目服务状态
MQ_QUEUE_MSG = 'QUEUE_MSG'  # 日志
MQ_QUEUE_EXEC = 'QUEUE_EXEC'  # 执行功能
MQ_QUEUE_MAIL = 'QUEUE_MAIL'  # 邮件任务

# 主机配置信息
HOST = None  # 主机名，主机IP
PORT = None  # 启动端口
CONTEXT = None  # 项目上下文

ROOT_DB_DS = None  # 根数据源
ROOT_MQ_DS = None  # 根MQ源
ROOT_REDIS_DS = None  # 根redis源
ROOT_MAIL_DS = None  # 根mail源

ROOT_MQ_DEFAULT_QUEUE = None  # 根默认队列

# 上传路径
ROOT_UPLOAD_PATH = None  # 根上传路径

CONF_INFO = \
    {
    }

# code 代码表
CODE_INFO = \
    {
    }
from bin import init
from bin.base.tool import JsonFileFunc
from bin.base.data import Path
from bin.base.log import Logger
import os

J = JsonFileFunc.getInstance()
P = Path.getInstance()
L = Logger.getInstance('sys.log')


# 本地配置文件初始化
def sysConfInit():
    sysConfInfo = J.readFile(P.confDirPath + os.sep + 'conf.json')
    # 服务信息
    init.HOST = sysConfInfo.get('server').get('host')  # 服务ip
    init.PORT = sysConfInfo.get('server').get('port')  # 服务端口
    init.CONTEXT = sysConfInfo.get('server').get('context')  # 服务上下文

    # 根数据库信息
    init.ROOT_DB_DS = init.CONTEXT + 'mongodb'  # 根数据库源名称
    init.CONF_INFO[init.ROOT_DB_DS] = sysConfInfo.get('DB')  # 根数据库信息

    # 根redis信息
    init.ROOT_REDIS_DS = init.CONTEXT + 'redis'  # 根MQ源名称
    init.CONF_INFO[init.ROOT_REDIS_DS] = sysConfInfo.get('redis')  # 根数据库信息

    # 根MQ 信息
    init.ROOT_MQ_DS = init.CONTEXT + 'rabbitMQ'  # 根MQ源名称
    init.CONF_INFO[init.ROOT_MQ_DS] = sysConfInfo.get('rabbitMQ')  # 根MQ队列信息

    # MAIL 信息
    init.ROOT_MAIL_DS = init.CONTEXT + 'mail'  # 根邮件名称
    init.CONF_INFO[init.ROOT_MAIL_DS] = sysConfInfo.get('mail')  # 根mail信息

    # 根上传配置路径
    init.ROOT_UPLOAD_PATH = sysConfInfo.get('uploadPath')  # 系统配置上传路径


sysConfInit()
