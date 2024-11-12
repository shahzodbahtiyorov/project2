import requests
import json

from v1.helper.logger import Logger
from v1 import HUMO_URL, HUMO_TOKEN
import time
logging = logger = Logger(__name__, False, 10)
url = HUMO_URL
token = HUMO_TOKEN


def post(endpoind, method, params, timeout=None):
    start_time = time.time()
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": start_time,
        "method": method,
        "params": params
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url + endpoind, headers=headers, data=payload, timeout=(None, timeout))
    logging.api_service_request(payload, __name__, response, start_time)
    return response.json()
