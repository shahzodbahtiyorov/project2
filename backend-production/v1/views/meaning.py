#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

"""
meaning.py

This module contains the JSON-RPC method for handling encrypted requests in the meaning context.

Methods:
- `meaning(request)`: Processes an incoming JSON-RPC request by decrypting the data,
        validating the service, checking authorization, and dispatching the request.
    Returns an appropriate JSON response based on the request's outcome.

Dependencies:
- `ujson`: Used for parsing and encoding JSON data.
- `cryptography.fernet`: Used for encrypting and decrypting data with Fernet symmetric encryption.
- `django.core.cache`: Used for caching service data to improve performance.
- `django.http`: Provides HttpResponse and JsonResponse for returning HTTP responses.
- `django.views.decorators.csrf`: Provides csrf_exempt to bypass CSRF verification for this view.
- `jsonrpcserver`: Handles dispatching JSON-RPC requests.
- `v1.models.errors.Service`: Represents service status and activity in the database.
- `v1.models.users.AccessToken`: Represents user access tokens for authorization.
- `v1.services.logger`: Provides logging functionality for request and response details.
- `v1.utils.helpers.error_message`: Utility for generating standardized error messages.
- `v1.utils.validator.validator`: Used for validating request parameters.

"""

import datetime
import json
from re import compile as re_compile
import ujson as ujson
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import dispatch

from api import settings
from v1 import MEANING_URL_FERNET_KEY
from v1.helper.error_messages import MESSAGE
from v1.helper.logger import Logger
from v1.models.errors import Service
from v1.models.users import AccessToken
from v1.utils.helpers import error_message
from v1.utils.validator import validator
from cryptography.fernet import Fernet

fernet = Fernet(MEANING_URL_FERNET_KEY)
logger = Logger(__name__, False, 10)

# --------------------------- #
#       AUTHORIZATION
# --------------------------- #
AUTHORIZATION = ""

DISPATCH = ""


@csrf_exempt
# @view_logger(Logger('jsonrpc'))
def meaning(request):
    # Json decode Error Handler
    try:
        body = ujson.loads(request.body)
        if 'what' not in body:
            return error_message(777, MESSAGE['serviceDown'], rpc=True, json_response=True)
        enc_data = body['what']

        # start decrypt request data
        decrypted = fernet.decrypt(enc_data.encode())
        original_string = decrypted.decode()
        # Replacing single quotes with double quotes to make it valid JSON
        json_string = original_string.replace("'", "\"")

        # Parsing the JSON string into a Python dictionary
        body = json.loads(json_string)
        json_data = json.dumps(body, indent=4)

        method_name = body['method']

        service = Service.objects.filter(method=method_name)
        if service.exists():
            if not service.first().is_active:
                return error_message(777, MESSAGE['serviceDown'], rpc=True, json_response=True)
        else:
            service = Service(method=method_name)
            service.save()

    except ValueError:
        return error_message(-32700, rpc=True, json_response=True)

    request_id = body.get('id')
    headers = request.headers
    firebase = headers.get("X-Firebase-AppCheck", "")
    version = headers.get("Version", "")
    uuid = headers.get("uuid", "")
    if method_name in [
        'client.home',
        'get.cert.auth',
        'get.cert.cms',
        'news.get.all',
        'news.get.single',
        'get.notifications',
        'get.reports',
        'make.transaction',
        'make.transaction.budget',
        'get.transaction',
        'get.mfo',
        'get.purpose.code',
        'get.sample',
        'get.document.details',
        'account.history',
        'company.staff',
        'statistic.chart',
        'get.budget.account',
        'get.budget.income.account',
        'get.account.details',
        'get.account.history',
        'get.account.name',
        'get.account.turnover',
        'get.account.active',
        'get.account.invoice',
        'get.account.turnover.total',
        'get.trash.info',
        'get.gas.info',
        'get.energy.info',
        'get.car.info',
        'get.mib.info',
    ]:
        log = {
            '\n--header--': headers,
            '\n--request--': json_data,
        }
    elif method_name == 'my.id.identification':
        log = {
            '\n--header--': headers,
            '\n--request--': {
                "jsonrpc": "2.0",
                "id": body['id'],
                "method": method_name,
                "params": {
                    "code": body['params']['code']
                }
            }
        }
    else:
        log = {
            '\n--header--': headers,
            '\n--request--': json_data,
            '\n--request_hash--': request.body.decode(),
        }
    logger.info(log)
    if version:
        q, w, e = version.split(".")
        q, w, e = int(q), int(w), int(e)
        print(q, w, e)
        if q < 1 or (q == 1 and w < 0) or (q == 1 and w == 0 and e < 0):
            return JsonResponse(
                {
                    "status": False,
                    "error": {
                        "message": {
                            "uz": "iltimos ilovani yangilang",
                            "ru": "пожалуйста, обновите приложение",
                            "en": "please update the app"
                        }
                    }})
        else:
            print("Versiya 2.2.95 yoki undan yuqori")

    else:
        res = {
            'login.user'
        }
        if method_name in res:
            res = res
        else:
            return JsonResponse({
                "status": False,
                "error": {
                    "message": {
                        "uz": "iltimos ilovani yangilang",
                        "ru": "пожалуйста, обновите приложение",
                        "en": "please update the app"
                    }
                }})

    if cache.get(f"serivces_{method_name}"):
        service = cache.get(f"serivces_{method_name}")
    else:
        service = Service.objects.filter(method=method_name).first()
        if service:
            cache.set(f"serivces_{method_name}", service, 86400)
            service = cache.get(f"serivces_{method_name}")
        else:
            service = Service(method=method_name)
            service.save()
            cache.set(f"serivces_{method_name}", service, 86400)
            service = cache.get(f"serivces_{method_name}")
    if not service.is_active:
        return error_message(500, rpc=True, json_response=True)

    # VALIDATE FIELDS
    validate = validator(body.get('params'))
    if 'error' in validate:
        return JsonResponse(validate, safe=False)
    context = {
        'request_id': request_id,
        'X-Firebase-AppCheck': firebase,
        'version': version,
    }
    # Authorization
    if method_name not in settings.NO_LOGIN_METHODS:
        authorization = headers.get('Authorization', '')
        pattern = re_compile(r"Bearer (.+)")

        if not pattern.match(authorization):
            return error_message(-32102, rpc=True, json_response=True)

        input_token = pattern.findall(authorization)[0]

        # Authorize
        try:
            token: AccessToken = AccessToken.objects.get(key=input_token)
            user = token.user
            if uuid and version:
                device = user.device.filter(core_id=uuid).first()
                if device:
                    if device.version != version:
                        device.version = version
                        device.save()
            context["user"] = user
            context["token"] = input_token
        except AccessToken.DoesNotExist:
            return HttpResponse("Unauthorized", status=401)

    # DISPATCH
    data = ujson.loads(dispatch(json_data, context=context))
    if method_name in [
        'client.home',
    ]:
        log = {
            '\n--header--': headers,
            '\n--request--': json_data,
        }
    elif method_name == 'my.id.identification':
        log = {
            '\n--header--': headers,
            '\n--request--': {
                "jsonrpc": "2.0",
                "id": body['id'],
                "method": method_name,
                "params": {
                    "code": body['params']['code']
                }
            },
            '\n--response--': data,
        }
    else:
        log = {
            '\n--header--': headers,
            '\n--request--': json_data,
            '\n--response--': data,
            '\n--request_hash--': request.body.decode(),
        }
    logger.info(log)
    data['status'] = 'result' in data
    data['origin'] = method_name
    data['host'] = {
        'host': settings.APP_NAME,
        'timestamp': str(datetime.datetime.now())
    }

    return HttpResponse(ujson.dumps(data).encode(), content_type="application/json")
