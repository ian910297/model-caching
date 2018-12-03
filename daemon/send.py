import asyncio
import concurrent.futures
import requests
import sys
import json
import random
from os.path import abspath, expanduser, basename
from glob import glob

#with open(abspath(expanduser('~/model-caching/config/node.json')), 'r') as src:
#    node = json.loads(src.read())

#hosts = []
#for i in range(len(node)):
#    hosts.append(node[i]['host'])

host = 'http://' + sys.argv[1] + ':5001'
model_root_path = '~/model_root_backup'
model_root_dir = abspath(expanduser(model_root_path))
model_names = [basename(x) for x in glob(model_root_dir + '/*.model')]

MAX_WORKER = 6
async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        loop = asyncio.get_event_loop()
        
        modelname = random.choice(model_names)
        url = '{}/get-model/{}'.format(host, modelname)
        futures = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url
            )
            for i in range(MAX_WORKER)
        ]
        for response in await asyncio.gather(*futures):
            print(response.content)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    i = 0
    while i < 3:
        loop.run_until_complete(main())
        i += 1