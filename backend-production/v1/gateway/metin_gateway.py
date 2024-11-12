import json

import requests
from v1 import METIN_URL


def post(cms):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url=METIN_URL, json=cms, headers=headers)
    print(f'METIN RESPONSE: {response.status_code}, {response.text}')
    return json.loads(response.json())
