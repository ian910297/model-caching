from flask import Flask, request, jsonify
from os.path import abspath, expanduser
import requests
import time
import json
import sys

sys.path.insert(0, abspath(expanduser('~/model-caching/service_wrapper')))
sys.path.insert(0, abspath(expanduser('~/model-caching/Multi-interfaceFileFetcher')))
# service wrapper
from controller.server_controller import ServerController
# model getter
from ModelGetter.ModelGetter import ModelGetter

app = Flask(__name__)
with open(abspath(expanduser('~/model-caching/config/path.json')), 'r') as src:
    path = json.loads(src.read())
server = ServerController(path)

@app.route("/call-node/<filename>")
def call_node(filename="mlp.model"):
    res = requests.get('http://localhost:5001/build-model/' + filename)
    if res.ok:
        print(res)
        print('ok')
    else:
        print('error')
    
    return "OK"

@app.route("/build-model/<modelname>/<unit>/<epoch>")
def build_model(modelname, unit, epoch):
    pass

@app.route("/test-async")
def test_async():
    res = requests.get('http://localhost:5001/test-async')
    if res.ok:
        print(res)
        print('ok')
    else:
        print('error')
    
    return "OK"

def main():
    global app
    global server

    # launch RESTful server
    # app.debug = True
    # app.run(host='localhost', port=5000)

if __name__ == "__main__":
    main()
