from os.path import abspath, expanduser, basename
from glob import glob
from subprocess import Popen, PIPE
import time
import random

# service wrapper
from controller.base_controller import BaseController
# model getter
from ModelGetter.ModelGetter import ModelGetter

class ServerController(BaseController):
    def __init__(self, path):
        self.path = path
        self.model_script_dir = abspath(expanduser(path['model_script_dir']))
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
        # check that exist the required model on the node
        
    
    def build_model(self, filename='mlp.unit5.epoch50.model'):
        print('build model')
        self.status = 'build model'
        PYTHON = 'python3'
        EXECUTE_SCRIPT = self.model_script_dir + '/train_mnist.py'
        execute_command = [PYTHON, EXECUTE_SCRIPT, '--filename', filename]
        p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

        # wait for the process to terminate
        # or use p.wait() to wait
        out, err = p.communicate()

        self.status = 'build model end'

        return 200

    def eval(self, task):
        if task is '2-CNN':
            return 1, -1
        elif task is '3-CNN':
            return 3, -1
        else:
            return 1, -1
        
