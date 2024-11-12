UZCARD = 0
HUMO = 1
VISA_USD = 2
TCB_CARD = 3
PAYGINE_CARD = 4
COIN_SUM = 19
COIN_USD = 20
VISA_SUM = 22
UNIRED = 29
MOMENT = 30


def get_name(type):
    name_map = {
        0: 'UZCARD',
        1: 'HUMO',
        2: 'VISA_USD',
        3: 'TCB_CARD',
        4: 'PAYGINE_CARD',
        19: 'COIN_SUM',
        20: 'COIN_USD',
        22: 'VISA_SUM',
        29: 'UNIRED',
        30: 'MOMENT'
    }
    return name_map.get(type, 'Unknown Type')


def get_id(type):
    id_map = {
        'UZCARD': 0,
        'HUMO': 1,
        'VISA_USD': 2,
        'TCB_CARD': 3,
        'PAYGINE_CARD': 4,
        'COIN_SUM': 19,
        'COIN_USD': 20,
        'VISA_SUM': 22,
        'UNIRED': 29,
        'MOMENT': 30
    }
    return id_map.get(type, -1)
