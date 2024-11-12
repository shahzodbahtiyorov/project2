#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

import requests
import json
import time

from v1 import SMS_URL, SMS_TOKEN


def post(mobile, text):
    start_time = time.time()
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": start_time,
        "method": "send.sms",
        "params":
            {
                "phone": mobile,
                "content": text
            }

    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SMS_URL
    }
    requests.post(SMS_TOKEN, headers=headers, data=payload, timeout=10)

    return {
        "status": True,
        "result": True
    }
