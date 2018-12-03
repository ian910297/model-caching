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
with open(abspath(expanduser('~/model-caching/config/node.json')), 'r') as src:
    node = json.loads(src.read())
server = ServerController(node)

@app.route("/build-model/<modelname>/<unit>/<epoch>")
def build_model(modelname, unit, epoch):
    pass

def main():
    global app
    global server

    # launch RESTful server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
