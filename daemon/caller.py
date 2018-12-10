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
    
    con = Controller(node)

    req_sim = RequestSimulator(60, 2.)
    file_freq = []
    while len(file_freq)<1000:
        file_freq = req_sim.generate_file_popularity()
    time_period = req_sim.generate_time_period()
    #for i in range(len(time_period)):
    for i in range(100):
        record = {}
        record['task_assign'] = time.time()
        record['modelname'] = req_sim.model_names[file_freq[i]]
        print('[{}] Request: {}'.format(i, record['modelname']))
        con.task_queue.put(record)
        time.sleep(time_period[i])
    

    # stop worker
    for i in range(4):
        con.task_queue.put(None)
    for i in range(len(con.bosses)):
        boss = con.bosses[i]
        for j in range(len(boss.workers)):
            boss.workers[j].join()
    print('output data')
    con.export()
    

    
if __name__ == "__main__":
    main()