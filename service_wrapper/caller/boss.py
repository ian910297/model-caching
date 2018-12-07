from queue import Queue
from threading import Thread
from caller.task import do_work

class Boss():
    def __init__(self, host, task_queue, out_queue, __MAX_TASK=2, __MAX_WORKER=2):
        self.__MAX_WORKER = __MAX_WORKER
        self.host = host
        self.score = 0
        self.task_queue = task_queue
        self.out_queue = out_queue
        self.score_queue = Queue()
        self.workers = self.__init_workers()
        self.task_size = __MAX_TASK
    
    def __init_workers(self):
        workers = []
        for i in range(self.__MAX_WORKER):
            t = Thread(target=do_work, args=(self.host, self.task_queue, self.score_queue, self.out_queue))
            t.start()
            workers.append(t)
    
        return workers

    def update_score(self):
        while not self.score_queue.empty():
            self.score += self.score_queue.get()