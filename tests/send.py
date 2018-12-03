import requests
import json
import random
from os.path import abspath, expanduser, basename
from glob import glob
from threading import Thread
from queue import Queue

#hosts = []
#for i in range(len(node)):
#    hosts.append(node[i]['host'])

model_root_path = '~/model_root_backup'
model_root_dir = abspath(expanduser(model_root_path))
model_names = [basename(x) for x in glob(model_root_dir + '/*.model')]

def pack(data):
    output = []
    for i in range(len(data)):
        record = data[i]
        timestamp = json.loads(record[1])

        new = {}
        new['url'] = record[0]
        new['modelname'] = new['url'].split('/')[-1]
        new['request_time'] = timestamp['request_time']
        new['download_time'] = timestamp['download_time']
        output.append(new)
    
    return output


def export(url):
    res = requests.get(url)
    if res.ok:
        return str(res.content)
    else:
        return 'ERROR'

def do_work(url):
    res = requests.get(url)
    if res.ok:
        #print('[OK]', res.json())
        return str(res.json())
    else:
        #print('[ERROR]')
        return 'ERROR'

def worker(q, host):
    data = []
    while True:
        url = q.get()
        if url is None:
            url = 'http://{}:5001/export'.format(host)
            export(url)

            data = pack(data)
            with open(host+'.json', 'w') as src:
                src.write(json.dumps(data))
            break
        res = do_work(url)
        data.append([url, res])
        q.task_done()

def boss(host, num_worker_threads=4, times=100):
    # assign task to worker
    worker_threads = []
    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker, args=(q, host))
        t.start()
        worker_threads.append(t)
    
    # generate task queue for worker
    global model_names
    for i in range(times):
        modelname = random.choice(model_names)
        url = 'http://{}:5001/get-model/{}'.format(host, modelname)
        q.put(url)
    q.join()

    # stop worker
    for i in range(num_worker_threads):
        q.put(None)
    for t in worker_threads:
        t.join()

def controller():
    with open(abspath(expanduser('~/model-caching/config/node.json')), 'r') as src:
        node = json.loads(src.read())
    
    # create boss thread to manage worker
    boss_threads = []
    for i in range(len(node)):
        t = Thread(target=boss, args=(node[i]['host'], 2, 10))
        t.start()
        boss_threads.append(t)
    
    # wait boss()
    for t in boss_threads:
        t.join()

if __name__ == "__main__":
    controller()