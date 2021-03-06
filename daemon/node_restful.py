"""
Are global variables thread safe in flask? How do I share data between requests?
https://stackoverflow.com/a/32825482

Not only is it not thread safe, it's not process safe ......
I would implement my cache mechanism with Queue()
"""
from flask import Flask, request, jsonify
from os.path import abspath, expanduser
from queue import Queue
import requests
import time
import json
import sys

sys.path.insert(0, abspath(expanduser('~/model-caching/service_wrapper')))
sys.path.insert(0, abspath(expanduser('~/model-caching/Multi-interfaceFileFetcher')))
from ModelGetter.ModelGetter import ModelGetter
from controller.node_controller import NodeController

app = Flask(__name__)
with open(abspath(expanduser('~/model-caching/config/path.json')), 'r') as src:
    path = json.loads(src.read())
node = NodeController(path, 'Softmax')
@app.route("/inference/<unit>/<modelname>")
def inference(unit, modelname):
    global node
    unit = int(unit)
    request_start = time.time()
    download_time = 0

    if node.is_cache(modelname) == False:
        download_start = time.time()
        # download model
        node.get_model(modelname)
        download_end = time.time()
        download_time = download_end - download_start

    inference_start = time.time()
    # inference
    result = node.inference(unit, modelname)
    inference_end = time.time()
    
    # cache update
    node.cache_update(modelname)
    request_end = time.time()

    inference_time = inference_end - inference_start
    request_time = request_end - request_start

    res = {}
    res['result'] = result
    res['node_request_start'] = str(request_start)
    res['request_time'] = str(request_time)
    res['download_time'] = str(download_time)
    res['inference_time'] = str(inference_time)
    res = json.dumps(res)

    return jsonify(res)

@app.route("/get-model/<modelname>")
def get_model(modelname):
    global node
    request_start = time.time()
    download_time = 0

    if node.is_cache(modelname) == False:
        download_start = time.time()
        # download
        node.get_model(modelname)
        download_end = time.time()
        download_time = download_end - download_start

    # cache update
    node.cache_update(modelname)
    request_end = time.time()
    request_time = request_end - request_start

    res = {}
    res['node_request_start'] = str(request_start)
    res['request_time'] = str(request_time)
    res['download_time'] = str(download_time)
    res = json.dumps(res)

    return jsonify(res)

@app.route("/export")
def export():
    global node
    node.export()

    return 'export success'

def main():
    global app
    global node

    app.debug = False
    app.run(host='0.0.0.0', processes=1, threaded=False)
    #app.run(host='0.0.0.0', processes=1, threaded=True)

if __name__ == "__main__":
    main()