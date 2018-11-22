from flask import Flask, request, jsonify
import time
import json
import asyncio
from os.path import abspath, expanduser
import sys
import requests
import threading

sys.path.insert(0, abspath(expanduser('~/model-caching/Multi-interfaceFileFetcher')))
from ModelGetter.ModelGetter import ModelGetter
from node_controller import NodeController

app = Flask(__name__)
loop = asyncio.get_event_loop()
node = NodeController('~/model_root', '~/model-caching/model')

@app.route("/build-model/<filename>")
def build_model(filename):
    print("filename is", filename)
    global node
    status_code = node.build_model(filename)
    
    #p = threading.Thread(target = node.build_model)
    #p.start()
    #p.join()

    return "OK"

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

@app.route("/test-async")
def test_async():
    #event = threading.Event()
    #callback_with_event = functools.partial(callback, test_async_tool)
    #loop.run_until_complete(test_async_tool)
    threads = []
    for i in range(2):
        threads.append(threading.Thread(target = my_sleep, args = (i, 5)))
        threads[i].start()
    
    for i in range(2):
        threads[i].join()

    return "OK"

def main():
    global app
    app.debug = True
    app.run(host='localhost', port=5001)


if __name__ == "__main__":
    main()