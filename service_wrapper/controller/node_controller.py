from os.path import abspath, expanduser, basename
from glob import glob
from subprocess import Popen, PIPE
import chainer

# service wrapper
from controller.base_controller import BaseController
from model.mlp import MLP
# model getter
from ModelGetter.ModelGetter import ModelGetter

class NodeController(BaseController):
    def __init__(self, path):
        self._path = path
        self.model_list = self.model_list(path['model_root_dir'])

        # Model Getter
        self._store_node_config = self.load_config(path['store_node_config'])
        self.if_desc = self.extract_config(self._store_node_config, path['shell_script_dir'])
        self.p_desc = 'Dummy'
        self.mg = ModelGetter(interface_descriptors=self.if_desc, policy_descriptor=self.p_desc)

        self.model_script_path = abspath(expanduser(path['model_script_dir']))
        self.tasks = []
        self.__MAX_TASK = 2
   
    def test_getter(self, round_end):
        cnt = 0
        while cnt < round_end:
            target_model = random.choice(["mlp.unit5.epoch5.model", "mlp.unit5.epoch10.model"])

            start = time.time()
            self.mg.GetModel(target_model)
            end = time.time()
            cnt += 1
            print("[Round {}][Cost {}]".format(cnt, end - start))
    
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
