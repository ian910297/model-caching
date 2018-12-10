import requests
import time
import json

def do_work(host, task_queue, score_queue, out_queue):
    while True:
        record = task_queue.get()
        
        if record is None:
            url = 'http://{}:5001/export'.format(host)
            break
        
        result = {}
        result['host'] = host
        result['modelname'] = record['modelname']
        result['url'] = 'http://{}:5001/get-model/{}'.format(host, record['modelname'])
        result['timestamp'] = {}
        result['timestamp']['task_assign'] = record['task_assign']
        result['timestamp']['task_start'] = time.time()
        response = requests.get(result['url'])
        if response.ok:
            timestamp = json.loads(response.json())
            result['timestamp']['node_request_start'] = timestamp['node_request_start']
            result['timestamp']['node_request_time'] = timestamp['request_time']
            result['timestamp']['download_time'] = timestamp['download_time']
            result['request_status'] = 'SUCCESS'
        else:
            result['request_status'] = 'ERROR'
        result['timestamp']['task_end'] = time.time()
        out_queue.put(result)

        