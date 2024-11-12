START = 0
DEFAULT = 1
PREMIUM = 2


def get_name(type_id):
    type_map = {
        1: 'DEFAULT',
        2: 'PREMIUM'
    }
    return type_map.get(type_id, 'START')
