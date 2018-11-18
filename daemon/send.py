import requests
import json as j

data = {
    "mytext": "hello, mytext"
}

res = requests.post('http://localhost:5000/', json=j.dumps(data))
if res.ok:
    print(res.json())
else:
    print('error')