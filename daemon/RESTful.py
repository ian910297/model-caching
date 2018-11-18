from flask import Flask, request, jsonify
from node import Node
import time
import json

app = Flask(__name__)
node = Node("p2p", "localhost", "p2p", "password")

@app.route("/", methods=['GET', 'POST'])
def hello():
    content = json.loads(request.json)
    print(content)

    global node
    print(node.name)
    node.name = content['mytext']
    node.status = 'busy'
    time.sleep(30)

    return jsonify({"data": "Hello, World!"})

@app.route("/get")
def check():
    global node
    if node.status is 'busy':
        return 'node is busy'
    else:
        return 'node is free'

if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)

