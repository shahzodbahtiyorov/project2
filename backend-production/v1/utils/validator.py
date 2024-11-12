#  Unisoft Group Copyright (c) 2022/12/5
#
#  Created by Muzaffar Makhkamov
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from v1.utils.helpers import error_message

fields = [
    'username',
    'password',
    'ext_id',
    'phone',
    'card_number',
    'card_token'
]


def validator(params):
    if isinstance(params, dict):
        for key, value in params.items():
            if key in fields:
                check = eval(f"{key}({repr(value)})")

                if check == True:
                    print(key)
                    continue
                else:
                    return error_message(500, f'{key}-{value}')
    elif isinstance(params, list):
        for param in params:
            for key, value in param.items():
                if key in fields:
                    check = eval(f"{key}({repr(value)})")

                    if check == True:
                        print(key)
                        continue
                    else:
                        return error_message(500, f'{params.index(param)}-{key}-{value}')

    return {"result": True}


def username(value):
    if len(value) > 50 or len(value) < 4:
        return error_message(-32700)
    return True


def password(value):
    if len(value) == 5:
        return error_message(-32700)
    return True


def ext_id(value):
    if len(value) > 50 or len(value) < 1:
        return error_message(-32700)
    return True


def phone(value):
    if len(value) != 12:
        return error_message(-32700)
    return True


def card_number(value):
    return True


def card_token(value):
    return True
