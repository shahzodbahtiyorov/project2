import json
import random

import requests

from v1 import EGOV_TOKEN, EGOV_BASE_URL


def egov_info(endpoint, data):
    url = EGOV_BASE_URL
    print(url)
    payload = json.dumps({
        'jsonrpc': '2.0',
        'method': 'egov.info',
        'params': {
            "endpoint": endpoint,
            "data": data
        },
        "id": random.randint(1, 10000)
    })
    print(payload)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {EGOV_TOKEN}'
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response.json()
