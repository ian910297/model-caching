import numpy as np
import collections
import json
import math
import random
from random import shuffle
from os.path import abspath, expanduser, basename
from glob import glob

class RequestSimulator:
    """
    _lambda means 
    """
    def __init__(self, dist_lambda=60, dist_alpga=2.):
        self.dist_alpha = dist_alpga
        self.dist_lambda = dist_lambda
        self.model_names = self.__init_modelnames()
    
    def __init_modelnames(self):
        """ Get Models """
        model_root_path = '~/model_root_backup'
        model_root_dir = abspath(expanduser(model_root_path))
        model_names = [basename(x) for x in glob(model_root_dir + '/*.model')]

        return model_names

    def generate_file_popularity(self, size=3000):
        """ Generate zipf distribution(zeta distribution) """
        s = np.random.zipf(self.dist_alpha, size)
        """ 
        How to count the occurrence of certain item in an ndarray in Python https://stackoverflow.com/a/28663910

        Two way to count the elements in a list
        1.
        unique, counts = np.unique(s, return_counts=True)
        counts = dict(zip(unique, counts))
        2.
        counts = collections.Counter()
        """
        
        return (s[s<(len(self.model_names) + 1)] - 1)

    def generate_time_period(self, size=100, dist='exp'):
        if dist is 'exp':
            time_period = [random.expovariate(self.dist_lambda)*60 for _ in range(size)]
        
        return time_period

