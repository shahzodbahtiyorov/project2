TRANSFER = 0
PAYMENT = 1
MTS_TRANSFER = 2
MTS_PAYMENT = 3
TCB_TRANSFER = 4
TCB_PAYMENT = 5
TCB_RF_TRANSFER = 6
CONVERSION = 7
VISA_TRANSFER = 8
COIN_TRANSFER = 9
TJ_TU_TRANSFER = 10
TJ_UT_TRANSFER = 11
ARMENIA_TRANSFER = 12
TURKEY_TRANSFER = 13
KAZAKH_TRANSFER = 14
AZR_TRANSFER = 15
SBP_TRANSFER = 16
VISA_DIRECT = 17
MTS_RF_PAYMENT = 18
PAGINE_TRANSFER = 19
GEORGIA_TRANSFER = 20
SCHOOL_TRANSFER = 21
VISA_UNIVERSAL_TRANSFER = 22
PAYGINE_UNIVERSAL_TRANSFER = 23
PAYMENT_BY_DETAILS_TRANSFER = 24
KIND_PAYMENT = 25
FREEDOM_TRANSFER = 26
SBP_QR = 27
BUDGET_TRANSFER = 28
ATTO_METRO_TRANSFER = 29
VISA_PAYMENT = 30
HUMO_ANOTHER_MONITORING = 31
UZCARD_ANOTHER_MONITORING = 32
SUBSCRIBE_TRANSFER = 33
VAQF_TRANSFER = 34
GME_TRANSFER = 35


def get_name(type_id):
    type_map = {
        0: 'TRANSFER',
        1: 'PAYMENT',
        2: 'MTS_TRANSFER',
        3: 'MTS_PAYMENT',
        4: 'TCB_TRANSFER',
        5: 'TCB_PAYMENT',
        6: 'TCB_RF_TRANSFER',
        7: 'CONVERSION',
        8: 'VISA_TRANSFER',
        9: 'COIN_TRANSFER',
        10: 'TJ_TU_TRANSFER',
        11: 'TJ_UT_TRANSFER',
        12: 'ARMENIA_TRANSFER',
        13: 'TURKEY_TRANSFER',
        14: 'KAZAKH_TRANSFER',
        15: 'AZR_TRANSFER',
        16: 'SBP_TRANSFER',
        17: 'VISA_DIRECT',
        18: 'MTS_RF_PAYMENT',
        19: 'PAGINE_TRANSFER',
        20: 'GEORGIA_TRANSFER',
        21: 'SCHOOL_TRANSFER',
        22: 'VISA_UNIVERSAL_TRANSFER',
        23: 'PAYGINE_UNIVERSAL_TRANSFER',
        24: 'PAYMENT_BY_DETAILS_TRANSFER',
        25: 'KIND_PAYMENT',
        26: 'FREEDOM_TRANSFER',
        27: 'SBP_QR',
        28: 'BUDGET_TRANSFER',
        29: 'ATTO_METRO_TRANSFER',
        30: 'VISA_PAYMENT',
        31: 'HUMO_ANOTHER_MONITORING',
        32: 'UZCARD_ANOTHER_MONITORING',
        33: 'SUBSCRIBE_TRANSFER',
        34: 'VAQF_TRANSFER',
        35: 'GME_TRANSFER',
    }
    return type_map.get(type_id, 'Unknown Type')


def get_id(type_name):
    id_map = {
        'TRANSFER': 0,
        'PAYMENT': 1,
        'MTS_TRANSFER': 2,
        'MTS_PAYMENT': 3,
        'TCB_TRANSFER': 4,
        'TCB_PAYMENT': 5,
        'TCB_RF_TRANSFER': 6,
        'CONVERSION': 7,
        'VISA_TRANSFER': 8,
        'COIN_TRANSFER': 9,
        'TJ_TU_TRANSFER': 10,
        'TJ_UT_TRANSFER': 11,
        'ARMENIA_TRANSFER': 12,
        'TURKEY_TRANSFER': 13,
        'KAZAKH_TRANSFER': 14,
        'AZR_TRANSFER': 15,
        'SBP_TRANSFER': 16,
        'VISA_DIRECT': 17,
        'MTS_RF_PAYMENT': 18,
        'PAGINE_TRANSFER': 19,
        'GEORGIA_TRANSFER': 20,
        'SCHOOL_TRANSFER': 21,
        'VISA_UNIVERSAL_TRANSFER': 22,
        'PAYGINE_UNIVERSAL_TRANSFER': 23,
        'PAYMENT_BY_DETAILS_TRANSFER': 24,
        'KIND_PAYMENT': 25,
        'FREEDOM_TRANSFER': 26,
        'SBP_QR': 27,
        'BUDGET_TRANSFER': 28,
        'ATTO_METRO_TRANSFER': 29,
        'VISA_PAYMENT': 30,
        'HUMO_ANOTHER_MONITORING': 31,
        'UZCARD_ANOTHER_MONITORING': 32,
        'SUBSCRIBE_TRANSFER': 33,
        'VAQF_TRANSFER': 34,
        'GME_TRANSFER': 35,
    }
    return id_map.get(type_name, -1)


def get_all():
    return {
        "list": [
            "TRANSFER",
            "PAYMENT",
            "MTS_TRANSFER",
            "MTS_PAYMENT",
            "TCB_TRANSFER",
            "TCB_PAYMENT",
            "TCB_RF_TRANSFER",
            "CONVERSION",
            "VISA_TRANSFER",
            "COIN_TRANSFER",
            "TJ_TU_TRANSFER",
            "TJ_UT_TRANSFER",
            "ARMENIA_TRANSFER",
            "TURKEY_TRANSFER",
            "KAZAKH_TRANSFER",
            "AZR_TRANSFER",
            "SBP_TRANSFER",
            "VISA_DIRECT",
            "MTS_RF_PAYMENT",
            "PAGINE_TRANSFER",
            "GEORGIA_TRANSFER",
            "SCHOOL_TRANSFER",
            "VISA_UNIVERSAL_TRANSFER",
            "PAYGINE_UNIVERSAL_TRANSFER",
            "PAYMENT_BY_DETAILS_TRANSFER",
            "KIND_PAYMENT",
            "FREEDOM_TRANSFER",
            "SBP_QR",
            "BUDGET_TRANSFER",
            "ATTO_METRO_TRANSFER",
            "GME_TRANSFER"
        ]
    }
