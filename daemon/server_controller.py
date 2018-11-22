
class ServerController():
    def __init__(self):
        self.nodes = []
        self.tasks = []
        self.__MAX_TASK_PER_NODE = 2
        self.__MAX_TASK = 0
    
    def add_node(self, name, data):
        self.nodes.append({'name': name, 'data': data, 'tasks': [], 'eval': 0})
        self.__MAX_TASK = len(self.nodes) * self.__MAX_TASK_PER_NODE

    def run(self, task):
        # eval task to figure out how many nodes this task would use
        node_num, node_eval  = self.eval(task)
        
        # choose node
        i = 0
        while i < node_num:
            for j in range(len(self.nodes)):
                if (len(self.nodes[j]['tasks']) < self.__MAX_TASK_PER_NODE) and (self.nodes[j]['eval'] > node_eval):
                    self.nodes[j]['tasks'].append(task)
                    break
            i = i + 1
        
        # execute task
        
    
    def eval(self, task):
        if task is '2-CNN':
            return 1, -1
        elif task is '3-CNN':
            return 3, -1
        else:
            return 1, -1
        
