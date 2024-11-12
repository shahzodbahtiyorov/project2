from v1.helper.logger import Logger

logger = Logger(__name__, False, 10)

debit_to_include = ['000', '4', 'APPROVED', 'ACWP', '3', 3, 4]
credit_to_include = ['PROCESSED', '4', '41', 4, 41, 'success']


def transfer_response(sms_response, monitoring):
    return {
        'otp_token': sms_response,
        "count": 5,
        'transfer': monitoring.collection()
    }
