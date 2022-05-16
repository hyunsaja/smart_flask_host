import requests
import json

url = 'http://localhost:3000/smart'
headers = {'Content-type': 'application/json; charset=utf-8'}
data = {
    'fname': 'smart',
    'cmd': 'camshot',
    'expos':'5000',
    'thickness':'15'
}

res = requests.post(url, headers=headers, data=json.dumps(data)).text
print(res)