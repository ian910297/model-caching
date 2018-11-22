from flask import Flask, request, jsonify
import time
import json
from os.path import abspath, expanduser
import sys
import requests

sys.path.insert(0, abspath('../Multi-interfaceFileFetcher'))
from ModelGetter.ModelGetter import ModelGetter
from server_controller import ServerController

app = Flask(__name__)
server = ServerController()

@app.route("/call-node/<filename>")
def call_node(filename="mlp.model"):
    res = requests.get('http://localhost:5001/build-model/' + filename)
    if res.ok:
        print(res)
        print('ok')
    else:
        print('error')
    
    return "OK"

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
    src = open('hosts.json', 'r')
    content = json.loads(src.read())
    for key, value in content.items():
        server.add_node(key, value)

    # launch RESTful server
    app.debug = True
    app.run(host='localhost', port=5000)

if __name__ == "__main__":
    main()
