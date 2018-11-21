class NodeController:
    def __init__(self, name, host, username, password):
        self.status = ''
        self.tasks = []
        self.__MAX_TASK = 2

    def run(self):
        # add task fail
        if len(self.tasks) < self.__MAX_TASK:
            return False
        
    
    def transmit_data(self):
        pass
