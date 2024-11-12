#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from datetime import datetime

from v1.gateway import metin_gateway
from v1.models.transaction import DocHistories


def statistic_chart(user, cms, month=None, year=None):
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
    if month and year:
        month = int(month)
        year = int(year)

        if not (1 <= month <= 12):
            return {"message": "Invalid month value. Must be between 1 and 12."}
        if year < 1:
            return {"message": "Invalid year value."}

        try:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
        except ValueError as e:
            return {"message": str(e)}

        charts = DocHistories.objects.filter(transaction_date__range=[start_date, end_date])
    else:
        charts = DocHistories.objects.all()

    result = [chart.collection() for chart in charts]

    kredit = [item for item in result if item.get('receiver_mfo') == '01186']
    total_kredit = sum(item.get('debit_amount', 0) for item in kredit)

    transfer = [item for item in result if item.get('receiver_mfo') == '00440']
    total_transfer = sum(item.get('debit_amount', 0) for item in transfer)

    withdraw = [item for item in result if item.get('receiver_mfo') == '00014']
    total_withdraw = sum(item.get('debit_amount', 0) for item in withdraw)

    transport = [item for item in result if item.get('receiver_mfo') == '01176']
    total_transport = sum(item.get('debit_amount', 0) for item in transport)

    others = [item for item in result if item.get('receiver_mfo') == '00421']
    total_others = sum(item.get('debit_amount', 0) for item in others)

    return {
        "result": [
            {
                "category": {
                    "uz": "Kreditlar",
                    "uzk": "Кредитлар",
                    "ru": "Кредиты",
                    "en": "Loans"
                },
                "amount": total_kredit,
                "color": "#079FEB"
            },
            {
                "category": {
                    "uz": "O'tkizmalar",
                    "uzk": "Уткизмалар",
                    "ru": "Переводы",
                    "en": "Transfers"
                },
                "amount": total_transfer,
                "color": "#8728E2"
            },
            {
                "category": {
                    "uz": "Naqt pul",
                    "uzk": "Накт пул",
                    "ru": "Cнятие",
                    "en": "Withdrawal"
                },
                "amount": total_withdraw,
                "color": "#FBAC66"
            },
            {
                "category": {
                    "uz": "Transport",
                    "uzk": "Транспорт",
                    "ru": "Транспорт",
                    "en": "Transport"
                },
                "amount": total_transport,
                "color": "#ebcc34"
            },
            {
                "category": {
                    "uz": "Boshqa",
                    "uzk": "Бошка",
                    "ru": "Другой",
                    "en": "Other"
                },
                "amount": total_others,
                "color": "#2A2A2E"
            }

        ]
    }
