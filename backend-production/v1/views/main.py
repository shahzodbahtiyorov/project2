#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import json
from re import compile as re_compile

import array
import ujson as ujson
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, dispatch

from api import settings
from v1.helper.error_messages import MESSAGE
from v1.models.errors import Service
from v1.models.users import AccessToken
from v1.services import auth, monitoring
from v1.utils.handlers import response_handler
from v1.utils.helpers import error_message
from v1.utils.validator import validator


# --------------------------- #
#       DB SERVICES
# --------------------------- #


# --------------------------- #
#       AUTHORIZATION
# --------------------------- #
AUTHORIZATION = ""


@method(name='auth.one')
# @count_requests(name='auth.one')
def auth_one(context, mobile: str, lang: str) -> Result:
    response = auth.one(mobile=mobile, lang=lang)
    return response_handler(response)


@method(name='auth.two')
# @count_requests(name='auth.two')
def auth_two(context, otp: str, otp_token: str) -> Result:
    response = auth.two(otp=otp, otp_token=otp_token)
    return response_handler(response)


@method(name='auth.register')
# @count_requests(name='auth.register')
def auth_register(context, otp_token: str, first_name: str, last_name: str, mobile: str, email: str, password: str,
                  details: array, promocode=None) -> Result:
    if "rel" in details["imei"] or "se" in details["imei"] or "infra" in details["imei"]:
        return response_handler({"error": "!!!!!!"})
    response = auth.register(otp_token=otp_token, first_name=first_name, last_name=last_name, mobile=mobile,
                             email=email, password=password, details=details)
    return response_handler(response)


@method(name='auth.login')
# @count_requests(name='auth.login')
def auth_login(context, otp_token: str, mobile: str, password: str, details: array) -> Result:
    if "rel" in details["imei"] or "se" in details["imei"] or "infra" in details["imei"]:
        return response_handler({"error": "!!!!!!"})
    response = auth.login(otp_token=otp_token, mobile=mobile, password=password, details=details)
    return response_handler(response)


@method(name="auth.forget.password.one")
# @count_requests(name='auth.forget.password.one')
def forget_password_one(context, mobile: str, lang: str) -> Result:
    response = auth.forget_password_one(mobile, lang)
    return response_handler(response)


@method(name="auth.forget.password.two")
# @count_requests(name='auth.forget.password.two')
def forget_password_two(context, otp: str, otp_token: str) -> Result:
    response = auth.forget_password_two(otp, otp_token)
    return response_handler(response)


@method(name="auth.change.password")
# @count_requests(name='auth.change.password')
def auth_change_password(context, mobile: str, new_password: str) -> Result:
    response = auth.auth_change_password(mobile, new_password)
    return response_handler(response)


# --------------------------- #
#       MONITORING
# --------------------------- #

@method(name="monitoring.all")
# @count_requests(name='monitoring.all')
def all(context, count: int, page: int, end=None, start=None) -> Result:
    response = monitoring.all(context['user'], count, page, end=end, start=start)
    return response_handler(response)


@method(name="monitoring.single")
# @count_requests(name='monitoring.single')
def single(context, count: int, page: int, token, start=None, end=None) -> Result:
    response = monitoring.single(context['user'], count, page, token, start, end)
    return response_handler(response)


DISPATCH = ""


@csrf_exempt
# @view_logger(Logger('jsonrpc'))
def jsonrpc(request):
    # Json decode Error Handler
    try:
        body = ujson.loads(request.body)

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
            # First try to get the token from the cache
            token = cache.get(input_token)

            # If the token wasn't in the cache, get it from the database and store it in the cache
            if token is None:
                token: AccessToken = AccessToken.objects.get(key=input_token)
                cache.set(input_token, token, 3600)  # cache for 1 hour
            user = token.user
            # if user.username == 'unired':
            #     # pass
            #     time.sleep(10)
            #     return error_message(-32103, rpc=True, json_response=True)
            context["user"] = user
            context["token"] = input_token
        except AccessToken.DoesNotExist:
            # return error_message(-32103, rpc=True, json_response=True)
            return HttpResponse("Unauthorized", status=401)
    # DISPATCH
    data = ujson.loads(dispatch(request.body.decode(), context=context))
    data['status'] = 'result' in data
    data['origin'] = method_name
    data['host'] = {
        'host': settings.APP_NAME,
        'timestamp': str(datetime.datetime.now())
    }

    return HttpResponse(ujson.dumps(data).encode(), content_type="application/json")
