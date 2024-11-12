#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from v1.models import AccessToken, Document_type, Device
from v1.models.home import Report, ClientInfo, ClientIABSAccount
from v1.gateway import shina_gateway, metin_gateway


def get_reports(user_token, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }

    access_token = AccessToken.objects.select_related('user').get(key=user_token)
    user = access_token.user
    if not user:
        return {
            "message": "User not found",
        }

    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    reports = Report.objects.filter(client=client).values('expense_article', 'created_at', 'client_id')

    for report in reports:
        if 'created_at' in report:
            report['created_at'] = report['created_at'].strftime('%d.%m.%Y')

    return {
        'result': list(reports)
    }


def client_home(user, device_id, cms):
    data = {
        "cms": cms
    }
    try:
        response = metin_gateway.post(data)
        if not response or 'revokeStatus' not in response:
            return {
                "result": {
                    "status": "500",
                    "message": "Service temporarily unavailable",
                    "is_revoked": False,
                }
            }

        if response['revokeStatus']:
            return {
                "result": {
                    "status": response['status'],
                    "message": response['message'],
                    "is_revoked": response['revokeStatus'],
                }
            }
    except Exception as e:
        return {
            "result": {
                "status": "500",
                "message": "Service temporarily unavailable",
                "is_revoked": False,
            }
        }
    print(device_id)
    device_access = Device.objects.select_related('user').get(user=user, core_id=device_id)
    print(device_access.name)
    if not device_access.verified:
        return {
            "result": {
                "message": "Access denied",
                "status": 401
            }
        }
    try:
        client_info = ClientInfo.objects.filter(user=user).first()
        print(client_info)
        if not client_info:
            return {
                "message": "User is not client",
            }
    except Exception as e:
        return {
            "result": {
                "message": "Service temporarily unavailable",
            }
        }

    client_accounts = ClientIABSAccount.objects.filter(client=client_info).select_related('client')
    accounts_list = [
        {
            "id": account.id,
            "number": account.number,
            "name": account.name,
            "saldo": account.balance,
            "primary": account.is_primary,
            "active": account.is_active,
            "is_document": account.is_document,
            "is_report": account.is_report,
            "inn": account.inn,
            "mfo": account.mfo,
            "iabs_id": account.iabs_id,
            "currency_code": account.currency_code,
            "code_coa": account.codeCoa,
            "created_at": account.created_accaunt_date.isoformat()
        }
        for account in client_accounts
    ]

    for account in accounts_list:
        endpoint = f'1.0.0/get-account-details?account={account["number"]}&code={account["mfo"]}&id={account["iabs_id"]}'

        try:
            gateway_response = shina_gateway.post("GET", endpoint)
            if gateway_response and gateway_response.get("code") == 0:
                gateway_balance = gateway_response["responseBody"]["saldo"]
                local_balance = account['saldo']
                if local_balance != gateway_balance:
                    account_instance = ClientIABSAccount.objects.get(id=account['id'])
                    account_instance.balance = gateway_balance
                    account_instance.save()
            else:
                return {
                    "result": {
                        "status": "500",
                        "message": "Service temporarily unavailable",
                    }
                }
        except Exception as e:
            return {
                "result": {
                    "status": "500",
                    "message": "Service temporarily unavailable",
                }
            }
    doc_type = [{"id": doc.id, "name": doc.name} for doc in Document_type.objects.all()]

    return {
        "result": {
            "client_code": client_info.client_code,
            "client_name": client_info.client_name,
            "branch_code": client_info.branch_code,
            "branch_name": client_info.branch_name,
            "devision_code": client_info.devision_code,
            "devision_name": client_info.devision_name,
            "direction_code": client_info.direction_code,
            "direction_name": client_info.direction_name,
            "contract_date": client_info.contract_date.isoformat(),
            "contract_number": client_info.contract_number,
            "director": client_info.director,
            "accountant": client_info.accountant,
            "is_active": client_info.is_active,
            "created_at": client_info.created_at.isoformat(),
            "updated_at": client_info.updated_at.isoformat(),
            "accounts": accounts_list,
            "doc_type": doc_type,
            "version": "1.0.0",
            "beta": True
        }
    }
