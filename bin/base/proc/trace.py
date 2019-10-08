from functools import wraps
from bin.base.log import Logger
import time


class trace(object):
    def __init__(self, logfile='trace.log', is_notify=False):
        self.logfile = logfile
        self.is_notify = is_notify

    def __call__(self, func):
        @wraps(func)
        def wraped_func(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            s = '%s 运行时间为:%.6f' % (func.__name__, (end_time - start_time))
            Logger.getInstance(self.logfile).info(s)
            return res

        return wraped_func

    def notify(self):
        print('调用提醒服务')
        pass
