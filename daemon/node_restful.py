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

@app.route("/use-model/<filename>")
def use_model(filename):
    print("filename is", filename)
    global node
    status_code = node.use_model(filename)

    return "OK"

@app.route("/status")
def status():
    global node

    return node.status

def my_sleep(num, second):
    print("Thread", num)
    time.sleep(second)



def main():
    global app
    global node
    shell_script_path= '../Multi-interfaceFileFetcher/scripts'

    #app.debug = True
    #app.run(host='localhost', port=5001)


if __name__ == "__main__":
    main()