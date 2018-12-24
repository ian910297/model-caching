from queue import Queue
from threading import Thread
from caller.task import get_model, inference

class Boss():
    def __init__(self, host, port, task_queue, out_queue, work='get_model', __MAX_WORKER=2):
        self.__MAX_WORKER = __MAX_WORKER
        self.host = host
        self.port = port
        self.score = 0
        self.task_queue = task_queue
        self.out_queue = out_queue
        self.score_queue = Queue()
        self.work = work
        self.workers = self.__init_workers()
    
    def __init_workers(self):
        workers = []
        for i in range(self.__MAX_WORKER):
            if self.work == 'get_model':
                t = Thread(target=get_model, args=(self.host, self.port, 
                       self.task_queue, self.score_queue, self.out_queue))
            elif self.work == 'inference':
                t = Thread(target=inference, args=(self.host, self.port, 
                       self.task_queue, self.score_queue, self.out_queue))
            t.start()
            workers.append(t)
    
        return workers

    def update_score(self):
        while not self.score_queue.empty():
            self.score += self.score_queue.get()