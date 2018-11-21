from flask import Flask, request, jsonify
import time
import json
from os.path import abspath
import sys

sys.path.insert(0, abspath('../Multi-interfaceFileFetcher'))
from ModelGetter.ModelGetter import ModelGetter
from node_controller import NodeController

app = Flask(__name__)
node = NodeController("p2p", "localhost", "p2p", "password")

@app.route("/assign-task")
def assign_task():
    global node
    

@app.route("/status")
def status():
    global node
    if node.status is 'busy':
        return 'node is busy'
    else:
        return 'node is free'

@app.route("/test", methods=['GET', 'POST'])
def hello():
    content = json.loads(request.json)
    print(content)

    global node
    print(node.name)
    node.name = content['mytext']
    node.status = 'busy'
    time.sleep(30)

    return jsonify({"data": "Hello, World!"})

def main():
    global app
    app.debug = True
    app.run(host='localhost', port=5000)


if __name__ == "__main__":
    
