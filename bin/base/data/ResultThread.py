import threading
import queue


class ResultThread(object):
    def __init__(self):
        self.res_queue = queue.Queue()
        self.func_queue = queue.Queue()

    def add_thread(self, func, kwargs):
        self.func_queue.put(threading.Thread(target=func, kwargs=kwargs))
        return self

    def set_result(self, result):
        self.res_queue.put(result)
        return self

    def start(self):
        for t in self.func_queue.queue:
            t.start()
        return self

    def join(self):
        for t in self.func_queue.queue:
            t.join()
        return self
