from os.path import abspath, expanduser, basename
from glob import glob
from subprocess import Popen, PIPE

class NodeController:
    def __init__(self, model_root_path, model_script_path):
        self.status = 'free'
        self.model_root_path = abspath(expanduser(model_root_path))
        self.model_names = [basename(x) for x in glob(self.model_root_path + '/*.model')]
        self.model_script_path = abspath(expanduser(model_script_path))
        self.tasks = []
        self.__MAX_TASK = 2

    def build_model(self, filename='mlp.model'):
        print('build model')
        self.status = 'build model'
        PYTHON = 'python3'
        EXECUTE_SCRIPT = self.model_script_path + '/train_mnist.py'
        execute_command = [PYTHON, EXECUTE_SCRIPT, '--filename', filename]
        p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

        # wait for the process to terminate
        # or use p.wait() to wait
        out, err = p.communicate()

        self.status = 'build model end'

        return 200
    
    def use_model(self, filename):
        self.status = 'use model'
        PYTHON = 'python3'
        EXECUTE_SCRIPT = self.model_script_path + '/inference_mnist.py'
        execute_command = [PYTHON, EXECUTE_SCRIPT, '--filename', filename]
        p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

        # wait for the process to terminate
        # or use p.wait() to wait
        out, err = p.communicate()
        
        self.status = 'use model end'
        return 200
        
    def transmit_data(self):
        pass
