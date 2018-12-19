import signal, os
from os.path import abspath, expanduser
import requests
import time
import json
import sys

# service wrapper
sys.path.insert(0, abspath(expanduser('~/model-caching/service_wrapper')))
from caller.controller import Controller
from caller.request_simulator import RequestSimulator

def main():
    with open(abspath(expanduser('~/model-caching/config/node.json')), 'r') as src:
        node = json.loads(src.read())

    with open(abspath(expanduser('~/model-caching/config/env.json')), 'r') as src:
        env = json.loads(src.read())
    
    _TASK_SIZE = env['_TASK_SIZE']
    _WORKER_PER_NODE = env['_WORKER_PER_NODE']
    _REQUEST_PER_MINUTE = env['_REQUEST_PER_MINUTE']
    _ZIPF_ALPHA = env['_ZIPF_ALPHA']

    con = Controller(node, _WORKER_PER_NODE)

    req_sim = RequestSimulator(_REQUEST_PER_MINUTE, _ZIPF_ALPHA)
    file_freq = []
    while len(file_freq) < _TASK_SIZE:
        file_freq = req_sim.generate_file_popularity(_TASK_SIZE * 8)
    time_period = req_sim.generate_time_period(_TASK_SIZE)
    for i in range(_TASK_SIZE):
        record = {}
        record['task_assign'] = time.time()
        record['modelname'] = req_sim.model_names[file_freq[i]]
        print('[{}] Request: {}'.format(i, record['modelname']))
        con.task_queue.put(record)
        time.sleep(time_period[i])
    

    # stop worker
    for i in range(len(con.bosses)):
        boss = con.bosses[i]
        for j in range(len(boss.workers)):
            con.task_queue.put(None)
    
    for i in range(len(con.bosses)):
        boss = con.bosses[i]
        for j in range(len(boss.workers)):
            boss.workers[j].join()
    print('output data')
    con.export()
    

    
if __name__ == "__main__":
    main()