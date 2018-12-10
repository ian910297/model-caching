import json
from queue import Queue

from caller.boss import Boss

class Controller():
    def __init__(self, nodes, policy='simple'):
        self.task_queue = Queue()
        self.out_queue = Queue()
        self.bosses = self.__init_bosses(nodes)
        self.tasks = [0] * len(nodes)
        self.policy = policy

    def __init_bosses(self, nodes):
        bosses = []
        for i in range(len(nodes)):
            #t = Boss(nodes[i]['host'], Queue(), self.out_queue)
            t = Boss(nodes[i]['host'], self.task_queue, self.out_queue)
            bosses.append(t)
        
        return bosses
    
    def export(self):
        data = []
        while not self.out_queue.empty():
            record = self.out_queue.get()
            timestamp = record['timestamp']
            
            result = {}
            result['task_waiting_time'] = float(timestamp['node_request_start']) - float(timestamp['task_assign'])
            result['task_time'] = float(timestamp['task_end']) - float(timestamp['task_start'])
            result['host'] = record['host']
            result['modelname'] = record['modelname']
            data.append(result)
        
        with open('output.json', 'w') as src:
            src.write(json.dumps(data))


    def assign_task(self, task):
        if(self.policy == 'simple'):
            sorted_by_score = sorted(self.bosses, lambda boss: boss['score'])
            print(sorted_by_score)
            for i in range(len(sorted_by_score)):
                pass