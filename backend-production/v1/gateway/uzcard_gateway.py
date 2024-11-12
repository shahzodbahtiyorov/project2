import requests
import json
import time

from django.http import HttpResponse
from v1 import UZCARD_URL, UZCARD_TOKEN
from v1.helper.logger import Logger
logging = logger = Logger(__name__, False, 10)
url = UZCARD_URL
token = UZCARD_TOKEN


def post(endpoind, method, params, timeout=None):
    try:
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
    except Exception as e:
        # Handle exceptions and return an error response
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


