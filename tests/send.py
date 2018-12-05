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
        record, response = data[i]
        timestamp = json.loads(response)

        new = {}
        new['host'] = record['host']
        new['url'] = record['url']
        new['modelname'] = record['modelname']
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

def worker(in_q, out_q, host):
    data = []
    while True:
        record = in_q.get()
        if record is None:
            url = 'http://{}:5001/export'.format(host)
            export(url)

            output = pack(data)
            out_q.put(output)
            break
        response = do_work(record['url'])
        data.append([record, response])
        in_q.task_done()

def boss(host, out_q, num_worker_threads=4, times=100):
    # assign task to worker
    worker_threads = []
    in_q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker, args=(in_q, out_q, host))
        t.start()
        worker_threads.append(t)
    
    # generate task queue for worker
    global model_names
    for i in range(times):
        modelname = random.choice(model_names)
        record = {}
        record['url'] = 'http://{}:5001/get-model/{}'.format(host, modelname)
        record['host'] = host
        record['modelname'] = modelname
        in_q.put(record)
    in_q.join()

    # stop worker
    for i in range(num_worker_threads):
        in_q.put(None)
    for t in worker_threads:
        t.join()

def controller():
    with open(abspath(expanduser('~/model-caching/config/node.json')), 'r') as src:
        node = json.loads(src.read())
    
    # create boss thread to manage worker
    boss_threads = []
    out_q = Queue()
    for i in range(len(node)):
        t = Thread(target=boss, args=(node[i]['host'], out_q))
        t.start()
        boss_threads.append(t)
    
    # wait boss()
    for t in boss_threads:
        t.join()
    
    # export result into a json
    out_q.put(None)
    data = []
    while True:
        output = out_q.get()
        if output is None:
            break
        
        for i in range(len(output)):
            data.append(output[i])
        out_q.task_done()

    with open('output.json', 'w') as src:
        src.write(json.dumps(data))
    

if __name__ == "__main__":
    controller()