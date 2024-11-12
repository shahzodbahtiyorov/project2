CREATED = 0
SUCCESS = 4
IN_PROCESS = 30
CANCELLED = 21


def get_description(state):
    if state == 0:
        return {
            "color": "#1976D2",
            "message": {
                "uz": "Yaratildi",
                "ru": "Создано",
                "en": "Created"
            }
        }
    if state == 4:
        return {
            "color": "#388E3C",
            "message": {
                "uz": "Muvaffaqiyatli",
                "ru": "Успех",
                "en": "Success"
            }
        }
    if state == 21:
        return {
            "color": "#d32f2f",
            "message": {
                "uz": "Bekor qilingan",
                "ru": "Отменено",
                "en": "Cancelled"
            }
        }
    if state == 21:
        return {
            "color": "#f6d809",
            "message": {
                "uz": "Jarayonda",
                "ru": "В процессе",
                "en": "In process"
            }
        }
    return {
        "color": "#f6d809",
        "message": {
            "uz": "Jarayonida",
            "ru": "В процессе",
            "en": "In process"
        }
    }


def get_visa_description(state):
    if state == 0:
        return {
            "color": "#1976D2",
            "message": {
                "uz": "Yaratildi",
                "ru": "Yaratildi",
                "en": "Yaratildi"
            }
        }
    if state == 4:
        return {
            "color": "#388E3C",
            "message": {
                "uz": "Muvaffaqiyatli",
                "ru": "Muvaffaqiyatli",
                "en": "Muvaffaqiyatli"
            }
        }
    if state == 21:
        return {
            "color": "#d32f2f",
            "message": {
                "uz": "Bekor qilingan",
                "ru": "Bekor qilingan",
                "en": "Bekor qilingan"
            }
        }
    return {
        "color": "#d32f2f",
        "message": {
            "uz": "Bekor qilingan",
            "ru": "Bekor qilingan",
            "en": "Bekor qilingan"
        }
    }
