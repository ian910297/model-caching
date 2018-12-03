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
    def __init__(self, nodes, policy='simple'):
        #self.path = path
        #self.model_script_dir = abspath(expanduser(path['model_script_dir']))
        self.nodes = nodes
        self.tasks = [0] * len(nodes)
        self.__MAX_TASK_PER_NODE = 5
        self.policy = policy

    def select_node(self, task):
        if(self.policy == 'simple'):
            for i in range(len(self.tasks)):
                if self.tasks[i] < self.__MAX_TASK_PER_NODE:
                    self.tasks[i] += 1
                    return i
            
            return -1
        
    
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
        
