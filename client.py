import requests
import pprint
import json

url = 'http://127.0.0.1:8000/smart'
headers = {'Content-type': 'application/json; charset=utf-8'}
data = {
    'user': 'smart',
    'cmd': 'cmd',
    'temp':'5000',
    'thickness':'15'
}

res = requests.post(url, headers=headers, data=json.dumps(data))
pprint.pprint(res.json())