from datetime import datetime

from django.db.models import Q, Sum

from v1.gateway import metin_gateway
from v1.models import MFO, AccessToken, PurposeCode, Sample, Report, ClientIABSAccount, ClientInfo, DocHistories, \
    BudgetAccount, BudgetIncomeAccount, Device


def account_history(user, device_id, account_number, cms, start_date=None, end_date=None):
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
    accounts = ClientIABSAccount.objects.filter(number=account_number).first()
    if not accounts:
        return {
            "message": "Account does not exist",
        }

    transactions = DocHistories.objects.filter(
        Q(sender_company_account=account_number) | Q(receiver_company_account=account_number)
    )

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
            transactions = transactions.filter(transaction_date__gte=start_date)
        except ValueError:
            return {
                "message": "Invalid start_date format. Use DD-MM-YYYY."
            }

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
            transactions = transactions.filter(transaction_date__lte=end_date)
        except ValueError:
            return {
                "message": "Invalid end_date format. Use DD-MM-YYYY."
            }

    result = []

    for transaction in transactions:
        transaction_data = {
            'transaction_date': transaction.transaction_date.strftime('%d-%m-%Y'),
        }

        if transaction.receiver_company_account == account_number:
            transaction_data['receiver_company_account'] = transaction.receiver_company_account
            transaction_data['receiver'] = transaction.receiver_name
            transaction_data['receiver_mfo'] = transaction.receiver_mfo
            transaction_data['receiver_inn'] = transaction.receiver_inn
            transaction_data['details'] = transaction.details
            transaction_data['status'] = transaction.status
            transaction_data['credit_amount'] = transaction.credit_amount if transaction.credit_amount else 0
        if transaction.sender_company_account == account_number:
            transaction_data['sender_company_account'] = transaction.sender_company_account
            transaction_data['sender_company'] = transaction.sender_company
            transaction_data['sender_mfo'] = transaction.sender_company_mfo
            transaction_data['sender_inn'] = transaction.sender_company_inn
            transaction_data['details'] = transaction.details
            transaction_data['status'] = transaction.status
            transaction_data['debit_amount'] = transaction.debit_amount if transaction.debit_amount else 0

        if 'receiver_company_account' in transaction_data or 'sender_company_account' in transaction_data:
            result.append(transaction_data)

    total_debit = transactions.filter(sender_company_account=account_number).aggregate(Sum('debit_amount'))[
                      'debit_amount__sum'] or 0
    total_credit = transactions.filter(receiver_company_account=account_number).aggregate(Sum('credit_amount'))[
                       'credit_amount__sum'] or 0

    return {
        "result": {
            "total_debit": total_debit,
            "total_credit": total_credit,
            "operations": result
        }}


def get_mfo(user_token, cms):
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
            "message": "User does not exist",
        }

    mfos = MFO.objects.all().values('code', 'name')

    return {
        'result': list(mfos)
    }


def get_purpose_code(user_token, cms):
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
            "message": "User does not exist",
        }

    purpose_codes = PurposeCode.objects.all().values('code', 'name')

    return {
        'result': list(purpose_codes)
    }


def get_sample(user_token, cms):
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
            "message": "User does not exist",
        }

    samples = Sample.objects.all().values('receiver_company', 'details', 'transfer_amount')

    return {
        "result": list(samples)
    }


def get_document_details(user, device_id, cms):
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
    if not user:
        return {"message": "User does not exist"}

    client = ClientInfo.objects.filter(user=user).first()
    print(client)
    if not client:
        return {"message": "Client not found"}
    sender_account = ClientIABSAccount.objects.select_related('client').filter(client=client).first()
    print(sender_account.name)
    if not sender_account:
        return {"message": "Account not found for the client"}

    transactions = DocHistories.objects.filter(
        Q(sender_company=sender_account.name) | Q(receiver_name=sender_account.name)
    ).values(
        'id',
        'sender_company',
        'sender_company_account',
        'sender_company_mfo',
        'sender_company_inn',
        'receiver_name',
        'receiver_company_account',
        'receiver_mfo',
        'receiver_inn',
        'transaction_date',
        'contract_number',
        'details',
        'status',
        'credit_amount',
        'debit_amount',
        'is_credit'
    )
    result = []
    for transaction in transactions:
        if transaction.get('is_credit') == 3:
            transaction['status'] = 'Ошибка'

        if transaction.get('sender_company') == sender_account.name:
            transaction['is_credit'] = 1
        else:
            transaction['is_credit'] = 2

        if transaction.get('transaction_date'):
            transaction['transaction_date'] = transaction['transaction_date'].strftime('%Y-%m-%d')
        result.append(transaction)

    return {
        "result": result
    }


def get_budget_account(user, code, cms):
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
    budget_account = BudgetAccount.objects.filter(code=code).first()
    if not budget_account:
        return {
            "result": {
                "en": "Budget does not exist",
                "ru": "Несуществующий бюджет",
                "uz": "Mavjud bo'lmagan byudjet"
            }
        }

    return {
        "result": {
            "code": budget_account.code,
            "name": budget_account.name,
            "tin": budget_account.tin,
        }
    }


def get_budget_income_account(user, code, cms):
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
    budget_income_account = BudgetIncomeAccount.objects.filter(code=code).first()
    if not budget_income_account:
        return {
            "result": {
                "en": "Budget does not exist",
                "ru": "Несуществующий бюджет",
                "uz": "Mavjud bo'lmagan byudjet"
            }
        }

    return {
        "result": {
            "code": budget_income_account.code,
            "name": budget_income_account.name,
            "coato": budget_income_account.coato,
            "region_code": budget_income_account.region_code,

        }
    }
