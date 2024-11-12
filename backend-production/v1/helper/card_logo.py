def get_logo(bin):
    logo_map = {
        0: '/img/card_logo/uzcard.png',
        1: '/img/card_logo/humo.png',
        2: '/img/card_logo/Virtual_USD.png',
        22: '/img/card_logo/Virtual_UZS.png',
        29: '/img/card_logo/wallet.png',
        30: '/img/card_logo/moment.png'
    }
    return logo_map.get(bin, 'default_logo_path')

