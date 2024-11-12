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
import firebase_admin
import ujson as ujson
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials
from jsonrpcserver import method, Result, dispatch

from api import settings
from v1.helper.error_messages import MESSAGE
from v1.helper.privacy import PRIVACY
from v1.models.errors import Service
from v1.models.users import AccessToken
from v1.services import monitoring, identification, news, home, permissions, notifications, card, document, menu, \
    auth_two, auth, accounts, government
from v1.utils.handlers import response_handler
from v1.utils.helpers import error_message
from v1.utils.validator import validator
from ubank_auth_server.services import client


# --------------------------- #
#       AUTHORIZATION
# --------------------------- #

@method(name="login.user")
def get_user_login(context, username, password, certificate, device_info) -> Result:
    response = auth_two.user_login(username, password, certificate, device_info)
    return response_handler(response)


@method(name="change.pass")
def change_password(context, current_pass, new_pass, cms) -> Result:
    response = auth_two.change_password(context['user'], current_pass, new_pass, cms)
    return response_handler(response)


@method(name="change.mandatory.pass")
def change_mandatory_password(context, new_password) -> Result:
    response = auth_two.change_mandatory_password(context['user'], new_password)
    return response_handler(response)


# --------------------------- #
#       METIN
# --------------------------- #

@method(name="get.cert.auth")
def get_cert_codes(context, otp_code, pin_code) -> Result:
    response = auth_two.get_cert_codes(context['user'], otp_code, pin_code)
    return response_handler(response)


@method(name="get.cert.cms")
def get_cert_cms(context, cms) -> Result:
    response = auth_two.get_cert_cms(context['user'], cms)
    return response_handler(response)


# --------------------------- #
#       NEWS
# --------------------------- #


@method(name="news.get.all")
def news_get_all(context, cms) -> Result:
    response = news.get_all(context['token'], cms)
    return response_handler(response)


@method(name="news.get.single")
def news_get_single(user_id, news_id, cms) -> Result:
    response = news.get_single(user_id, news_id, cms)
    return response_handler(response)


# --------------------------- #
#       FIREBASE
# --------------------------- #


@method(name="get.notifications")
def get_notifications(context, cms) -> Result:
    response = news.get_notification(context['token'], cms)
    return response_handler(response)


# --------------------------- #
#       CARD_REGISTER
# --------------------------- #

@method(name="uzcard.register.one")
def uzcard_register_one(user_id, card_number, expire, lang) -> Result:
    response = card.register_uzcard_one(user_id, card_number, expire, lang)
    return response_handler(response)


@method(name="uzcard.register.two")
def uzcard_register_two(user_id, name, card_number, expire, primary, otp, otp_token, card_id) -> Result:
    response = card.register_uzcard_two(user_id, name, card_number, expire, primary, otp, otp_token, card_id)
    return response_handler(response)


@method(name="humo.register.one")
def humo_register_one(user_id, card_number, expire, lang) -> Result:
    response = card.register_humo_one(user_id, card_number, expire, lang)
    return response_handler(response)


@method(name="humo.register.two")
def humo_register_two(user_id, name, card_number, expire, primary, otp, otp_token, card_id) -> Result:
    response = card.register_humo_two(user_id, name, card_number, expire, primary, otp, otp_token, card_id)
    return response_handler(response)


# --------------------------- #
#       Company_home
# --------------------------- #


@method(name="get.reports")
def get_reports(context, cms) -> Result:
    response = home.get_reports(context['token'], cms)
    return response_handler(response)


@method(name="client.request")
def add_client(context, phone, user_type, pass_front, pass_back, cms, pinfil=None, inn=None, licence=None,
               order_proxy=None) -> Result:
    response = client.add_client(phone, user_type, pass_front, pass_back, cms, pinfil, inn, licence,
                                 order_proxy)
    return response_handler(response)


@method(name="client.home")
def client_home(context, device_id, cms) -> Result:
    response = home.client_home(context['user'], device_id, cms)
    return response_handler(response)


# --------------------------- #
#       TRANSACTION
# --------------------------- #


@method(name="make.transaction")
def make_transaction(context, device_id, doc_num, doc_date, doc_type, sender_account, sender_mfo, sender_name,
                     sender_tax,
                     receiver_account, receiver_mfo, receiver_name, receiver_tax, purpose_code, purpose_sp_code,
                     purpose_name, amount, cms) -> Result:
    response = accounts.make_transaction(context['user'], device_id, doc_num, doc_date, doc_type, sender_account,
                                         sender_mfo,
                                         sender_name, sender_tax,
                                         receiver_account, receiver_mfo, receiver_name, receiver_tax, purpose_code,
                                         purpose_sp_code,
                                         purpose_name, amount, cms)
    return response_handler(response)


@method(name="make.transaction.budget")
def make_transaction(context, device_id, doc_num, doc_date, doc_type, sender_name, sender_account, sender_mfo,
                     sender_tax, budget_account,
                     purpose_code, purpose_sp_code, purpose_name, amount, cms, receiver_tax=None) -> Result:
    response = accounts.account_2_budget(context['user'], device_id, doc_num, doc_date, doc_type, sender_name,
                                         sender_account, sender_mfo,
                                         sender_tax, budget_account, purpose_code,
                                         purpose_sp_code, purpose_name, amount, cms, receiver_tax)
    return response_handler(response)


@method(name="get.transaction")
def get_transaction(context, tr_id) -> Result:
    response = accounts.get_transaction(context['user'], tr_id)
    return response_handler(response)


# --------------------------- #
#       MY ID
# --------------------------- #


@method(name="my.id.identification")
def my_id_identification(context, code, image, cms) -> Result:
    response = identification.my_id_identification_create(context['user'], code, image, cms)
    return response_handler(response)


@method(name="user.has.one.id")
def check_user_has_one_id(context, cms) -> Result:
    response = identification.my_id_user_info(context['user'], cms)
    return response_handler(response)


# --------------------------- #
#       Documents
# --------------------------- #

@method(name="get.mfo")
def get_mfo(context, cms) -> Result:
    response = document.get_mfo(context['token'], cms)
    return response_handler(response)


@method(name="get.purpose.code")
def get_purpose_codes(context, cms) -> Result:
    response = document.get_purpose_code(context['token'], cms)
    return response_handler(response)


@method(name="get.sample")
def get_sample(context, cms) -> Result:
    response = document.get_sample(context['token'], cms)
    return response_handler(response)


@method(name="get.document.details")
def get_document_details(context, device_id, cms) -> Result:
    response = document.get_document_details(context['user'], device_id, cms)
    return response_handler(response)


@method(name="account.history")
def account_history(context, device_id, account_number, cms, start_date=None, end_date=None) -> Result:
    response = document.account_history(context['user'], device_id, account_number, cms, start_date, end_date)
    return response_handler(response)


@method(name="company.staff")
def company_staff(context, cms) -> Result:
    response = menu.company_staff(context['token'], cms)
    return response_handler(response)


@method(name="statistic.chart")
def statistic_chart(context, cms, month=None, year=None) -> Result:
    response = monitoring.statistic_chart(context['token'], cms, month, year)
    return response_handler(response)


@method(name="get.budget.account")
def get_budget_account(context, code, cms) -> Result:
    response = document.get_budget_account(context['token'], code, cms)
    return response_handler(response)


@method(name="get.budget.income.account")
def get_budget_account(context, code, cms) -> Result:
    response = document.get_budget_income_account(context['token'], code, cms)
    return response_handler(response)


# --------------------------- #
#       Active Accounts
# --------------------------- #


@method(name="get.account.details")
def account_details(context, account, codeFilial, id, cms) -> Result:
    response = accounts.get_account_details(context['token'], account, codeFilial, id, cms)
    return response_handler(response)


@method(name="get.account.history")
def account_history(context, pk, dateBegin, dateClose, cms) -> Result:
    response = accounts.get_account_history(context['token'], pk, dateBegin, dateClose, cms)
    return response_handler(response)


@method(name="get.account.name")
def account_name(context, codeFilial, account, clientCode, cms) -> Result:
    response = accounts.get_account_name(context['token'], codeFilial, account, clientCode, cms)
    return response_handler(response)


@method(name="get.account.turnover")
def account_turnover(context, id, account, codeFilial, pageNumber, pageSize, type, dateBegin, dateClose, cms) -> Result:
    response = accounts.get_account_turnover(context['token'], id, account, codeFilial, pageNumber, pageSize, type,
                                             dateBegin, dateClose, cms)
    return response_handler(response)


@method(name="get.account.active")
def account_active(context, id, cms) -> Result:
    response = accounts.get_active_accounts(context['token'], id, cms)
    return response_handler(response)


@method(name="get.account.invoice")
def account_invoice(context, account, codeFilial, quantity, cms) -> Result:
    response = accounts.get_account_invoice(context['token'], account, codeFilial, quantity, cms)
    return response_handler(response)


@method(name="get.account.turnover.total")
def account_turnover_total(context, id, dateBegin, dateClose, cms) -> Result:
    response = accounts.get_account_turnover_total(context['token'], id, dateBegin, dateClose, cms)
    return response_handler(response)


# --------------------------- #
#       Active Accounts
# --------------------------- #


@method(name="get.trash.info")
def get_trash_info(context, cad_num, time, cms) -> Result:
    response = government.get_garbage_info(context['token'], cad_num, time, cms)
    return response_handler(response)


@method(name="get.gas.info")
def get_gas_info(context, tin, cms) -> Result:
    response = government.get_gas_info(context['token'], tin, cms)
    return response_handler(response)


@method(name="get.energy.info")
def get_gas_info(context, ptin, cms) -> Result:
    response = government.get_energy_info(context['token'], ptin, cms)
    return response_handler(response)


@method(name="get.car.info")
def get_car_info(context, device_id, cms) -> Result:
    response = government.get_car_info(context['user'], device_id, cms)
    return response_handler(response)


@method(name="get.mib.info")
def get_mib_info(context, tin, cms) -> Result:
    response = government.get_mib_info(context['token'], tin, cms)
    return response_handler(response)


DISPATCH = ""


@csrf_exempt
def backend(request):
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

        try:
            token = cache.get(input_token)

            if token is None:
                token: AccessToken = AccessToken.objects.get(key=input_token)
                cache.set(input_token, token, 3600)
            user = token.user
            context["user"] = user
            context["token"] = input_token
        except AccessToken.DoesNotExist:
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
