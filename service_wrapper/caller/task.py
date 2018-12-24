import requests
import time
import json

def get_model(host, port, task_queue, score_queue, out_queue):
    while True:
        record = task_queue.get()
        
        if record is None:
            url = 'http://{}:{}/export'.format(host, port)
            break
        
        result = {}
        result['host'] = host
        result['modelname'] = record['modelname']
        result['url'] = 'http://{}:{}/get-model/{}'.format(host, port, record['modelname'])
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

def inference(host, port, task_queue, score_queue, out_queue):
    while True:
        record = task_queue.get()
        
        if record is None:
            url = 'http://{}:{}/export'.format(host, port)
            break
        
        result = {}
        result['host'] = host
        result['modelname'] = record['modelname']
        result['url'] = 'http://{}:{}/inference/{}/{}'.format(host, port, record['unit'], record['modelname'])
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
