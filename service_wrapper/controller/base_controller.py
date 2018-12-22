from os.path import abspath, expanduser, basename
from glob import glob
import json

class BaseController:
    def __init__(self):
        pass

    def get_model_list(self, model_root_path):
        model_root_dir = abspath(expanduser(model_root_path))
        model_names = [basename(x) for x in glob(model_root_dir + '/*.model')]

        return model_names

    def load_config(self, config_path):
        with open(abspath(expanduser(config_path)), 'r') as src:
            config_obj = json.loads(src.read())
    
        return config_obj
    
    def extract_config(self, config_obj, shell_script_path):
        if_desc = []
    
        for n in config_obj.keys():
    
            if_info = config_obj[n]
            if 'wifi' not in if_info.keys():
                continue
    
            #if_desc.append('Scp,' + n + '_scp,'+ if_info['wifi'] + ',' + 
            #                    if_info['model_root'] + ',' + shell_script_path)
            if_desc.append('Ftp,' + n + '_ftp,'+ if_info['wifi'] + ',' +
                                 if_info['model_root'] + ',' + shell_script_path)
    
            if 'bluetooth' in if_info.keys():
                if_desc.append('Bluetooth,' + n + '_bt,'+ if_info['wifi'] + ',' +
                if_info['bluetooth'][0] +  ',' + if_info['bluetooth'][1] + ',model_root,'+ shell_script_path)
    
        return if_desc
    
