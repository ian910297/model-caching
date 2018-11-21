from flask import Flask, request, jsonify
import time
import json
from os.path import abspath
import sys

sys.path.insert(0, abspath('../Multi-interfaceFileFetcher'))
from ModelGetter.ModelGetter import ModelGetter
from server_controller import ServerController

app = Flask(__name__)
server = ServerController()

@app.route("/assign-task")
def assign_task():
    pass
    
@app.route("/list-node")
def status():
    pass

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
