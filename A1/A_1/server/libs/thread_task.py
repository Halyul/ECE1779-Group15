import threading

class ThreadTask(threading.Thread):
    def __init__(self, task, args=(), kwargs={}):
        threading.Thread.__init__(self)
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.task(*self.args, **self.kwargs)
        except Exception as e:
            print(self.name, e)