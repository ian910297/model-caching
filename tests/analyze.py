from os.path import abspath, expanduser, basename
from glob import glob
import json

current_dir = abspath('.')
json_files = [basename(x) for x in glob(current_dir + '/*.json')]

for i in range(len(json_files)):
    print(json_files[i])
    with open(json_files[i], 'r') as src:
        print(src)
        data = json.loads(src.read())