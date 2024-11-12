def get_description(state):
    state_descriptions = {
        0: {
            "color": "#1976D2",
            "message": {
                "uz": "Yaratildi",
                "ru": "Создано",
                "en": "Created"
            }
        },
        1: {
            "color": "#4eac5b",
            "message": {
                "uz": "Jarayonda",
                "ru": "В ходе выполнения",
                "en": "In progress"
            }
        },
        2: {
            "color": "#4eac5b",
            "message": {
                "uz": "Jarayonda",
                "ru": "В ходе выполнения",
                "en": "In progress"
            }
        },
        3: {
            "color": "#1a69f5",
            "message": {
                "uz": "Karta chiqish jarayonida",
                "ru": "Карта находится в процессе оформления",
                "en": "The card is in the process of registration"
            }
        },
        4: {
            "color": "#388E3C",
            "message": {
                "uz": "Muvaffaqiyatli",
                "ru": "Успех",
                "en": "Success"
            }
        },
        -1: {
            "color": "#d32f2f",
            "message": {
                "uz": "Bekor qilingan",
                "ru": "Отменено",
                "en": "Cancelled"
            }
        },
        -2: {
            "color": "#d32f2f",
            "message": {
                "uz": "Bekor qilingan",
                "ru": "Отменено",
                "en": "Cancelled"
            }
        },
        -3: {
            "color": "#d32f2f",
            "message": {
                "uz": "Bekor qilingan",
                "ru": "Отменено",
                "en": "Cancelled"
            }
        }
    }

    # Return the description for the state or a default one if state is unknown
    return state_descriptions.get(state, {
        "color": "#d32f2f",
        "message": {
            "uz": "Noma'lum holat",
            "ru": "Неизвестное состояние",
            "en": "Unknown status"
        }
    })
