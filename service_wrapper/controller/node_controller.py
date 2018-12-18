from os.path import abspath, expanduser, basename
from glob import glob
import time
import random
import numpy as np
import json

# chainer
import chainer
import chainer.functions as F
import chainer.links as L
from model.mlp import MLP

# service wrapper
from controller.base_controller import BaseController
# model getter
from ModelGetter.ModelGetter import ModelGetter

class NodeController(BaseController):
    def __init__(self, path, p_desc='Dummy', cache_size=2):
        self._path = path
        #self.model_list = self.get_model_list(path['model_root_dir'])
        self.cache_list = {}
        self.model_dict = {}
        self.cache_size = cache_size
        _, self.test = chainer.datasets.get_mnist()

        # Model Getter
        self._store_node_config = self.load_config(path['store_node_config'])
        self.if_desc = self.extract_config(self._store_node_config, path['shell_script_dir'])
        self.p_desc = p_desc
        self.mg = ModelGetter(interface_descriptors=self.if_desc, policy_descriptor=self.p_desc)
    
    def get_model(self, modelname):
        #print(self.if_desc)
        self.mg.GetModel(modelname)

    def inference(self, unit, modelname):
        print(unit)
        print(modelname)

        model = L.Classifier(MLP(unit, 10))
        # Load weight
        model_root_dir = abspath(expanduser(self._path['model_root_dir']))
        #print('{}/{}'.format(model_root_dir, modelname))
        chainer.serializers.load_npz('{}/{}'.format(model_root_dir, modelname), model)

        # Run inference
        test_index = random.randint(1, len(self.test))
        x = chainer.Variable(np.asarray([self.test[test_index][0]])) # test data 
        t = chainer.Variable(np.asarray([self.test[test_index][1]])) # labels
        y = model.predictor(x).data # inference result
        pred_label = y.argmax(axis=1)

        print('test index:', test_index)
        print('The test data label:', self.test[test_index][1])
        print('result:', pred_label[0])
        if int(self.test[test_index][1]) is int(pred_label[0]):
            return 'correct'
        else:
            return 'failed'
    
    def cache_update(self, modelname):
        if modelname not in self.model_dict.keys():
            self.model_dict[modelname] = {}
            self.model_dict[modelname]['frequency'] = 0
            self.model_dict[modelname]['timestamp'] = []
        self.model_dict[modelname]['frequency'] += 1
        self.model_dict[modelname]['timestamp'].append(time.time())

        
        # directly insert
        if len(self.model_dict.items()) < self.cache_size:
            self.cache_list[modelname] = self.model_dict[modelname]

        # Cache Most Frequency those popular model
        sorted_by_value = sorted(self.cache_list.items(), 
                                    key=lambda item: (item[1]['frequency'], item[1]['timestamp'][-1]))
        i = 0
        while i < len(sorted_by_value):
            if self.model_dict[modelname]['frequency'] >= sorted_by_value[i][1]['frequency']:
                if modelname not in self.cache_list.keys():
                    del self.cache_list[sorted_by_value[i][0]]
                self.cache_list[modelname] = self.model_dict[modelname]
                
            i += 1

        if i < self.cache_size:
            self.cache_list[modelname] = self.model_dict[modelname]
    
    def export(self):
        filepath = abspath(expanduser('~/model_root'))
        filepath += '/out.json'
        with open(filepath, 'w') as src:
            src.write(json.dumps(self.mg.__policy_agent__.__action_map__))

