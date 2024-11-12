import json
import random
import requests

from v1 import SHINA_URL, SHINA_PASSWORD, SHINA_USERNAME


def get_token():
    payload = json.dumps({
        "username": SHINA_USERNAME,
        "password": SHINA_PASSWORD,
    })

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{SHINA_URL}getToken', data=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f'Error retrieving token: {response.status_code} - {response.text}')
        return None


def post(method, endpoint, data=None):
    token = get_token()
    if token is None:
        print("Failed to retrieve token, aborting request.")
        return None

    payload = json.dumps(data) if data else None

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'requestId': str(random.randint(100, 999999)),
        'Accept-Language': 'en'
    }
    print(f"Request URL: {SHINA_URL}{endpoint}")
    print(f"Payload Data: {payload}")
    response = requests.request(method, f'{SHINA_URL}{endpoint}', data=payload, headers=headers)
    return response.json()
