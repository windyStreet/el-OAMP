from functools import wraps


class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wraped_func(*args, **kwargs):
            log_str = func.__name__ + ' was called'
            print(log_str)
            with open(self.logfile, 'a') as opened_file:
                opened_file.write(log_str + '\n')
            self.notify()
            return func(*args, **kwargs)

        return wraped_func

    def notify(self):
        print('调用其他服务')
        pass


if __name__ == "__main__":
    @logit()
    def fun():
        print('xxx')
        
    x = fun()
    print(x)
