import uuid
import random
from datetime import datetime
from v1.gateway import shina_gateway, metin_gateway
from v1.helper.helper import get_budget_or_kazna_name
from v1.models import ClientInfo, DocHistories, Users, Device


def get_account_details(user, account, codeFilial, id, cms):
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
    endpoint = f'1.0.0/get-account-details?account={account}&code={codeFilial}&id={id}'
    result = shina_gateway.post("GET", endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": {
                'typeAccount': result['typeAccount'],
                'account': result['account'],
                'nameAcc': result['nameAcc'],
                'inn': result['inn'],
                'codeCurrency': result['codeCurrency'],
                'saldo': result['saldo'],
                'codeFilial': result['codeFilial'],
                'codeCoa': result['codeCoa'],
                'nameFilial': result['nameFilial'],
                'condition': result['condition'],
                'openDate': result['openDate'],
                'prOpen': result['prOpen'],
            }
        }
    return {
        "result": result
    }


def get_account_history(user, pk, dateBegin, dateClose, cms):
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
    endpoint = f'1.0.0/get-account-history/{pk}?dateBegin={dateBegin}&dateClose={dateClose}'
    result = shina_gateway.post('GET', endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            'result': {
                "date": result['date'],
                "nameAcc": result['nameAcc'],
                "codeFilial": result['codeFilial'],
                "account": result['account'],
                "purpose": result['purpose'],
                "debit": result['debit'],
                "credit": result['credit'],
                "numberTrans": result['numberTrans'],
                "type": result['type'],
            }
        }
    return {
        "result": result

    }


def get_account_name(user, codeFilial, account, clientCode, cms):
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
    endpoint = f'1.0.0/get-account-name?codeFilial={codeFilial}&account={account}&clientCode={clientCode}'
    result = shina_gateway.post("GET", endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": {
                'name': result['name']
            }
        }
    return {
        "result": result
    }


def get_account_turnover(user, id, account, codeFilial, pageNumber, pageSize, type, dateBegin, dateClose, cms):
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
    endpoint = f'1.0.0/get-account-turnover?id={id}&account={account}&codeFilial={codeFilial}&pageNumber={pageNumber}&pageSize={pageSize}&type={type}&dateBegin={dateBegin}&dateClose={dateClose}'
    result = shina_gateway.post("GET", endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": {
                "date": result['date'],
                "nameAcc": result['nameAcc'],
                "codeFilial": result['codeFilial'],
                "account": result['account'],
                "purpose": result['purpose'],
                "debit": result['debit'],
                "credit": result['credit'],
                "numberTrans": result['numberTrans'],
                "type": result['type'],
            }
        }
    return {
        "result": result
    }


def get_active_accounts(user, id, cms):
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
    endpoint = f'1.0.0/get-active-accounts/{id}'
    result = shina_gateway.post("GET", endpoint)
    print(result)
    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": result
        }
    return {
        "result": result

    }


def get_account_invoice(user, account, codeFilial, quantity, cms):
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
    endpoint = f'1.0.0/invoice-request?account={account}&codeFilial={codeFilial}&quantity={quantity}'
    result = shina_gateway.post("GET", endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": {
                "operDate": result['operDate'],
                "amount": result['amount'],
                "comment": result['comment'],
                "type": result['type'],
            }
        }
    return {
        "result": result
    }


def get_account_turnover_total(user, id, dateBegin, dateClose, cms):
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
    endpoint = f'1.0.0/get-account-turnover-total?id={id}&dateBegin={dateBegin}&dateClose={dateClose}'
    result = shina_gateway.post("GET", endpoint)

    if 'responseBody' in result:
        result = result['responseBody']
        return {
            "result": {
                "account": result['account'],
                "saldoBegin": result['saldoBegin'],
                "debit": result['debit'],
                "credit": result['credit'],
                "saldoEnd": result['saldoEnd'],
            }
        }
    return {
        "result": result
    }


def make_transaction(user, device_id, doc_num, doc_date, doc_type, sender_account, sender_mfo, sender_name, sender_tax,
                     receiver_account, receiver_mfo, receiver_name, receiver_tax, purpose_code, purpose_sp_code,
                     purpose_name, amount, cms):
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
    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    print(client)
    tr_user = Users.objects.get(username=user)
    print(tr_user)
    tr_documents = {
        "type": "106",
        "externalId": f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M")}-{uuid.uuid4().hex[:12]}',
        "docNum": doc_num,
        "docDate": doc_date,
        "sender": {
            "account": sender_account,
            "codeFilial": sender_mfo,
            "tax": sender_tax,
            "name": sender_name
        },
        "recipient": {
            "account": receiver_account,
            "codeFilial": receiver_mfo,
            "tax": receiver_tax,
            "name": receiver_name
        },
        "purpose": {
            "purposeCode": purpose_code,
            "code": purpose_sp_code,
            "name": purpose_name
        },
        "amount": amount
    }
    payload = {
        "documents": [tr_documents]
    }
    endpoint = f'1.0.0/transactions'
    result = shina_gateway.post("POST", endpoint, data=payload)

    if 'responseBody' in result:
        monitoring = DocHistories()
        monitoring.client = client
        monitoring.user = tr_user
        monitoring.tr_id = result['responseBody']['createdDocuments'][0]['transactionId']
        monitoring.ext_id = f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M%S")}-{uuid.uuid4().hex[:12]}'
        monitoring.sender_company = sender_name
        monitoring.sender_device = device_access.name
        monitoring.receiver_name = receiver_name
        monitoring.sender_company_account = sender_account
        monitoring.receiver_company_account = receiver_account
        monitoring.credit_amount = amount
        monitoring.credit_description = f"Received {amount} from {sender_name} (Account: {sender_account})"
        monitoring.debit_amount = amount
        monitoring.debit_description = f"Transferred {amount} to {receiver_name} (Account: {receiver_account})"
        monitoring.personal_account = None
        monitoring.personal_inn = None
        monitoring.sender_company_mfo = sender_mfo
        monitoring.sender_company_inn = sender_tax
        monitoring.number = doc_num
        monitoring.doc_type = doc_type
        monitoring.transaction_date = datetime.strptime(doc_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        monitoring.receiver_mfo = receiver_mfo
        monitoring.receiver_purpose_code = purpose_code
        monitoring.receiver_inn = receiver_tax
        monitoring.details = purpose_name
        monitoring.status = result['msg']
        monitoring.is_credit = 1
        monitoring.save()

        return {
            "result": result
        }
    monitoring = DocHistories()
    monitoring.client = client
    monitoring.user = tr_user
    monitoring.tr_id = random.randint(1000000000, 9999999999)
    monitoring.ext_id = f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M%S")}-{uuid.uuid4().hex[:12]}'
    monitoring.sender_company = sender_name
    monitoring.sender_device = device_access.name
    monitoring.receiver_name = receiver_name
    monitoring.sender_company_account = sender_account
    monitoring.receiver_company_account = receiver_account
    monitoring.credit_amount = amount
    monitoring.credit_description = f"Received {amount} from {sender_name} (Account: {sender_account})"
    monitoring.debit_amount = amount
    monitoring.debit_description = f"Transferred {amount} to {receiver_name} (Account: {receiver_account})"
    monitoring.personal_account = None
    monitoring.personal_inn = None
    monitoring.sender_company_mfo = sender_mfo
    monitoring.sender_company_inn = sender_tax
    monitoring.number = doc_num
    monitoring.doc_type = doc_type
    monitoring.transaction_date = datetime.strptime(doc_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    monitoring.receiver_mfo = receiver_mfo
    monitoring.receiver_purpose_code = purpose_code
    monitoring.receiver_inn = receiver_tax
    monitoring.details = purpose_name
    monitoring.status = result['msg']
    monitoring.is_credit = 3
    monitoring.save()
    return {
        "result": result
    }


def account_2_budget(user, device_id, doc_num, doc_date, doc_type, sender_name, sender_account, sender_mfo, sender_tax,
                     budget_account, purpose_code, purpose_sp_code,
                     purpose_name, amount, cms, receiver_tax=None):
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
    print(get_budget_or_kazna_name(budget_account))
    endpoint = f'1.0.0/paymentToBudget'
    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    print(client)
    tr_user = Users.objects.get(username=user)
    print(tr_user)
    tr_documents = {
        "type": "106",
        "externalId": f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M")}-{uuid.uuid4().hex[:12]}',
        "docNum": doc_num,
        "docDate": doc_date,
        "sender": {
            "account": sender_account,
            "codeFilial": sender_mfo,
            "tax": sender_tax,
        },
        "budget": {
            "account": budget_account,
            "tax": receiver_tax,
        },
        "purpose": {
            "purposeCode": purpose_code,
            "code": purpose_sp_code,
            "name": purpose_name
        },
        "amount": amount
    }
    payload = {
        "documents": [tr_documents]
    }

    result = shina_gateway.post("POST", endpoint, data=payload)
    print(result)
    if 'responseBody' in result:
        monitoring = DocHistories()
        monitoring.client = client
        monitoring.user = tr_user
        monitoring.tr_id = result['responseBody']['createdDocuments'][0]['transactionId']
        monitoring.ext_id = f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M%S")}-{uuid.uuid4().hex[:12]}'
        monitoring.sender_company = sender_name
        monitoring.sender_device = device_access.name
        monitoring.receiver_name = get_budget_or_kazna_name(budget_account).get('name')
        monitoring.sender_company_account = sender_account
        monitoring.receiver_company_account = budget_account
        monitoring.credit_amount = amount
        monitoring.credit_description = f"Received {amount} from {sender_name} (Account: {sender_account})"
        monitoring.debit_amount = amount
        monitoring.debit_description = f"Transferred {amount} to (Account: {budget_account})"
        monitoring.personal_account = None
        monitoring.personal_inn = None
        monitoring.sender_company_mfo = sender_mfo
        monitoring.sender_company_inn = sender_tax
        monitoring.number = doc_num
        monitoring.doc_type = doc_type
        monitoring.transaction_date = datetime.strptime(doc_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        monitoring.receiver_purpose_code = purpose_code
        monitoring.receiver_inn = receiver_tax if receiver_tax else get_budget_or_kazna_name(budget_account).get(
            'coato')
        monitoring.details = purpose_name
        monitoring.status = result['msg']
        monitoring.is_credit = 1
        monitoring.save()

        return {
            "result": result
        }
    monitoring = DocHistories()
    monitoring.client = client
    monitoring.user = tr_user
    monitoring.tr_id = random.randint(1000000000, 9999999999)
    monitoring.ext_id = f'MSB-T-{datetime.now().strftime("%d%m%Y%H%M%S")}-{uuid.uuid4().hex[:12]}'
    monitoring.sender_company = sender_name
    monitoring.sender_device = device_access.name
    monitoring.receiver_name = get_budget_or_kazna_name(budget_account).get('name')
    monitoring.sender_company_account = sender_account
    monitoring.receiver_company_account = budget_account
    monitoring.credit_amount = amount
    monitoring.credit_description = f"Received {amount} from {sender_name} (Account: {sender_account})"
    monitoring.debit_amount = amount
    monitoring.debit_description = f"Transferred {amount} to (Account: {budget_account})"
    monitoring.personal_account = None
    monitoring.personal_inn = None
    monitoring.sender_company_mfo = sender_mfo
    monitoring.sender_company_inn = sender_tax
    monitoring.number = doc_num
    monitoring.doc_type = doc_type
    monitoring.transaction_date = datetime.strptime(doc_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    monitoring.receiver_purpose_code = purpose_code
    monitoring.receiver_inn = receiver_tax if receiver_tax else get_budget_or_kazna_name(budget_account).get('coato')
    monitoring.details = purpose_name
    monitoring.status = result['msg']
    monitoring.is_credit = 3
    monitoring.save()
    return {
        "result": result
    }


def get_transaction(user, tr_id):
    endpoint = f'1.0.0/transactions/{tr_id}'
    result = shina_gateway.post("GET", endpoint)

    return {
        "result": result
    }
