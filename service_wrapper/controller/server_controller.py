from os.path import abspath, expanduser, basename
from glob import glob
from subprocess import Popen, PIPE
import time
import random
from threading import Thread
from queue import Queue

# service wrapper
from controller.base_controller import BaseController
# model getter
from ModelGetter.ModelGetter import ModelGetter

class ServerController(BaseController):
    def __init__(self, nodes, policy='simple'):
        #self.path = path
        #self.model_script_dir = abspath(expanduser(path['model_script_dir']))
    
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
        
