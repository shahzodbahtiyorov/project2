import json

import requests
import firebase_admin
import google.auth.transport.requests
from google.oauth2 import service_account
from firebase_admin import credentials, firestore

from v1 import FIREBASE_SCOPE, FIREBASE_URL

SERVICE_ACCOUNT_KEY = {
    "type": "service_account",
    "project_id": "unired-business",
    "private_key_id": "a8b5ac566657be5e11dc2b24291bc30f29439e5d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDWPoA9NAFVMHao\nExiI6dyUCrPxcmEft047zhFZYsND3hU7sBjPbi4eOpKWx/IwwjFpVpJn8m6zfdzd\nLt+XFyyZHbacBB0UruAybFxnz3/lX1kpniTUwMuN/esZMLLd347CRdGcCUX0iNrp\nqEo4Tc/U3LXY4vAjoFIGEDcaQJkawKPcp//kLhIa+5wS//yMOTTlD1qVdflfEx9Z\nkie6plL3/DzLLbuhy1saRMs+qjuKFBSQ+8FNZAsxBP+jPmtWTC/0XNDnVEJZnjQ6\nI0y08rpLYhqDomMkF7vs5bHmnaE9+BRgjSCuw2pmZAi6Jy4oPnfZYRJmz18aGN/h\nRN3JuPS3AgMBAAECggEAI5IS9pZo1j0KplMtUqYJYmb4g1DrQTnM+m73QHD+XIlF\n2zgclmwDqi8tYW1nD6NeUs/11N5SdOijv/FlXA+T7wQY6oRgU6vJO3X0TaQM5wdS\npW9FTDGKWlPbMb59JAtXB3hSGecMP1JtjjfLwtdgd0YBxzW+ixu2Ip2UmH47LU6a\n1d2oaJZMS6/TwDl5aOT7eVwWcqe9YKWIw+e7FcyC1QULk7n5dAYO0h9uTV32ix5c\nGcpt5d5dDQI+FX0Zv6EGHHU+iniqm7yTN98jbDAZ6y12vV8f23TIk58tNLnpeHql\nP97WN9nAEqy2lhogbAOaErOA/4NOK8HiWKnq6FjTeQKBgQDye1DfuGREuZdzI/M3\nmO9qW5hWSs+AY/O/2++/Q3lbmGcx1M80EVZ6tTtomnfzd55sHM0tGomEeLH+b/Nk\nsVabucCsKCxr3KsgoYkQse9nZ/XMLhAoP4vsro731I6KNxi4jq80v7oTA1uWn7Jx\n+su0rV+fDVPwzGz3f0FyO1m0vQKBgQDiMC4ohHgqXEhvO2P4TTlEMDZ8bYNkhtRV\nvXnG2Coayvyqk5zHRq/E1ws137DKJwBMh4JFzIEByETQyaC66qD7LD/8wc8vb2S8\n3TkbZTQR2j0KrHvru8IiGNGREJj0esncdGQedD+e2kYs0eebNmlfetT3tqSWZHHR\nB+vbHbrYgwKBgA2QXFvHYsR9ZT1pm2dWxL28Ve8tzCGwdagb03NtgNJg2hTthJGz\nDpVaofIeAeu6m0AM9GU7gMnKPpqvBHxzdxbK8z4uGR4HgAMZRiOK8ItmQ1eilADM\nXTVmJlUyrK6KmnVodeCLgQsjOvJYCJFbqB15PUoWYsWricTmd3C+ZSw5AoGBAL4V\nh3T9fo765tSzsJvnKg0oB2IiFp3QwXkcts5os1m45QXk74h42xYtMnqf9k6s4A9w\nggZuiqwYxdxA1ha/P3JWCaA8sAVJM/uUXn2rW0r1gP8LXUkKjWdiPBwROrmaxzHB\njrIZN64j+X2JGX7TB1L6Qye6Ei9hUlU8tvV50qBJAoGBAJZsCCT5eyCypX7/B8Mu\nG6vxQDNzER5leVOwBESlQln7iLsgJT+jN91KzihazxXWjZPIYbqmUQo0nFPFJe3y\nWTj4fCDC52wP8w83+ZDMQMyexwmhKNZzS1sv336OreS6sXMuXW7ZFdgZ15tfebVA\nvhUEYbZj4hWvzVnFRGB0YRZe\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-db1dt@unired-business.iam.gserviceaccount.com",
    "client_id": "111119242957739093739",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fgc9a%40unired-mobile-flutter.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
SCOPES = [FIREBASE_SCOPE]

# Initialize Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests."""
    credential = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_KEY, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credential.refresh(request)
    return credential.token


def send_notification(params):
    """Send a notification via Firebase Cloud Messaging."""
    access_token = _get_access_token()
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; UTF-8',
    }

    response = requests.post(
        url=FIREBASE_URL,
        headers=headers,
        data=json.dumps(params)
    )
    return response.json()
