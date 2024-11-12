#  Unisoft Group Copyright (c) 2022/12/5
#
#  Created by Muzaffar Makhkamov
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.core.cache import cache

import datetime

from django.http import JsonResponse

from api import settings
from v1.models import Error


def phone_mask(number):
    return number


def card_mask(number):
    mask = "{}********{}".format(number[:4], number[-5:])
    return mask


def error_message(code, message=None, origin="", request_id=None, wrapper=False, rpc=False, json_response=False,
                  rpc_error=False):
    data = cache.get(f'error_message_{code}')
    if not data:
        # Error message is not in cache, get from database
        error = Error.objects.filter(code=code)
        if error.exists():
            error = error.first()

            data = {
                "code": error.code,
                "message": message
            }
        else:
            if message is None:
                message = {
                    "uz": "Nomalum xatolik yuz berdi",
                    "ru": "Произошла неопределенная ошибка",
                    "en": "Undefined error occurred",
                }
                data = {
                    "code": code,
                    "message": message
                }
            else:
                data = {
                    "code": code,
                    "message": message
                }

        # Store data in cache for 1 day
        cache.set(f'error_message_{code}', data, 3600)

    if wrapper:
        data = {"error": data}

    if rpc:
        data = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": data,
            "status": False,
            "origin": origin,
            "host": {
                "host": settings.APP_NAME,
                "timestamp": str(datetime.datetime.now())
            }
        }

    if json_response:
        data = JsonResponse(data, safe=False)

    if rpc_error:
        from jsonrpcserver import Error as RpcError
        return RpcError(code, message)

    return data


def url_action_helper(service, test=False):
    pass


def card_history_tr_code(code):
    credis_codes = ["110", "111", "113", "114", "115", "206", "208", "225", "227", "229", "314", "315", "316", "614",
                    "11b", "11c", "11C", "11E", "11G", "11G", "11L", "11V", "31a", "31A", "31b", "31B", "31D", "31E",
                    "31G", "31K", "31R", "31W", "51a", "51c", "51G"]
    return code in credis_codes
