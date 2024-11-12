from v1.helper import transfer_type


def get_description(state):
    print(state, transfer_type.PAYMENT)
    if state in [transfer_type.TRANSFER, transfer_type.COIN_TRANSFER]:
        return {
            "uz": "O'tkazma",
            "ru": "Перевод денег",
            "en": "Transfer"
        }
    if state in [transfer_type.PAYMENT, transfer_type.SCHOOL_TRANSFER, transfer_type.PAYMENT_BY_DETAILS_TRANSFER]:
        return {
            "uz": "To'lov",
            "ru": "Оплата",
            "en": "Payment"
        }
    if state in [transfer_type.MTS_TRANSFER, transfer_type.TCB_TRANSFER, transfer_type.ARMENIA_TRANSFER,
                 transfer_type.TURKEY_TRANSFER, transfer_type.KAZAKH_TRANSFER, transfer_type.SBP_TRANSFER, transfer_type.VISA_UNIVERSAL_TRANSFER,
                 transfer_type.PAYGINE_UNIVERSAL_TRANSFER, transfer_type.FREEDOM_TRANSFER, transfer_type.SBP_QR]:
        return {
            "uz": "Xalqaro O'tkazma",
            "ru": "Международный перевод",
            "en": "International Transfer"
        }
    if state in [transfer_type.MTS_PAYMENT]:
        return {
            "uz": "Xalqaro To'lov",
            "ru": "Международный Оплата",
            "en": "International Payment"
        }
    if state in [transfer_type.CONVERSION]:
        return {
            "uz": "Valyuta ayriboshlash",
            "ru": "Kонвертация",
            "en": "Conversion"
        }
    return {
        "uz": "O'tkazma",
        "ru": "Перевод денег",
        "en": "Transfer"
    }
