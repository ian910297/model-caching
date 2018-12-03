from flask import Flask, request, jsonify
from os.path import abspath, expanduser
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
node = NodeController(path)

@app.route("/inference/<unit>/<modelname>")
def inference(unit, modelname):
    global node
    unit = int(unit)
    
    if modelname not in node.model_list:
        print('[WARNING] required model')
        print('Get the model')
        node.get_model(modelname)

    result = node.inference(unit, modelname)
    return result

@app.route("/get-model/<modelname>")
def get_model(modelname):
    global node

    download_time = 'not download'
    #print(node.model_history)
    if modelname not in node.cache_list:
        download_start = time.time()
        node.get_model(modelname)
        download_end = time.time()
        download_time = download_end - download_start

        print(download_time)

    node.cache_update(modelname)

    return str(download_time)

@app.route("/export")
def export():
    global node
    node.export()

    return 'export success'

def main():
    global app
    global node

    #app.debug = True
    app.run(host='0.0.0.0', port=5001)


if __name__ == "__main__":
    main()