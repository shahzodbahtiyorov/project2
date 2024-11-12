from datetime import datetime


def auth(code, lang):
    data = {
        'ru': f"Kode: {code}\n\nUnired Mobile\nVnimaniye! Ne soobshyayte etot kod postoronnim.(Sotrudniki UNIRED "
              f"NIKOGDA ne "
              "zaprashivayut kod)",
        'en': f"Code: {code}\n\nUnired Mobile\nAttention! Do not share this code with others.(UNIRED employees NEVER "
              f"ask for a "
              "code)",
        'uz': f"Kod: {code}\n\nUnired Mobile\nOgoh bo'ling! Ushbu parolni hech kimga bermang.(UNIRED xodimlari uni "
              f"HECH QACHON "
              "so'ramaydi)",
    }
    return data[lang]


def forget(code, lang):
    data = {
        'ru': f"Kode: {code}\n\nUnired Mobile\nVnimaniye! Ne soobshyayte etot kod postoronnim.(Sotrudniki UNIRED "
              f"NIKOGDA ne "
              "zaprashivayut kod)",
        'en': f"Code: {code}\n\nUnired Mobile\nAttention! Do not share this code with others.(UNIRED employees NEVER "
              f"ask for a "
              "code)",
        'uz': f"Kod: {code}\n\nUnired Mobile\nOgoh bo'ling! Ushbu parolni hech kimga bermang.(UNIRED xodimlari uni "
              f"HECH QACHON "
              "so'ramaydi)",
    }
    return data[lang]


def transfer(code, lang, card_number, amount, type):
    currency = 'SUM'
    if type == 'transfer-usd':
        currency = 'USD'
    elif type == "transfer-rub":
        currency = 'RUB'

    data = {
        'ru': f"Kode: {code}\n\nUnired Mobile\nUvazhayemyy kliyent, s Vashey {card_number} karty spisyvayetsya {amount / 100} {currency}. Vvedite kod dlya podtverzhdeniya.(Sotrudniki UNIRED NIKOGDA ne poprosyat ob etom)!",
        'en': f"Code: {code}\n\nUnired Mobile\nDear client, your {card_number} card is debited with {amount / 100} {currency}. Enter the confirmation code. (UNIRED employees will NEVER ask for this)!",
        'uz': f"Kod: {code}\n\nUnired Mobile\nXurmatli mijoz sizni {card_number} kartangizdan {amount / 100} {currency} miqdorida pul yechib olinmoqda. Tasdiqlash uchun kodni kiriting. (UNIRED xodimlari uni HECH QACHON so'ramaydi)!"
    }
    return data[lang]


def add_card(code, lang, card_number):
    data = {
        'ru': f"Kode: {code}\n\nUnired Mobile\nUvazhayemyy kliyent, s Vashey {card_number} karty dobavlyayetsya v "
              f"Unired Mobile App. Vvedite kod dlya podtverzhdeniya.(Sotrudniki UNIRED NIKOGDA ne poprosyat ob etom)!",
        'en': f"Code: {code}\n\nUnired Mobile\nDear client, your {card_number} card is adding to Unired Mobile App. "
              f"Enter the confirmation code. (UNIRED employees will NEVER ask for this)!",
        'uz': f"Kod: {code}\n\nUnired Mobile\nXurmatli mijoz sizni {card_number} kartangiz Unired Mobile ilovasiga "
              f"qo'shilmoqda. Tasdiqlash uchun kodni kiriting. (UNIRED xodimlari uni HECH QACHON so'ramaydi)!"
    }
    return data[lang]


def login(lang, mobile_name):
    current_datetime = datetime.now()
    data = {
        'ru': f"Войдите в учетную запись Unired Mobile " + current_datetime.strftime('%Y-%m-%d %H:%M:%S') + " " + mobile_name + "\nЕсли это не вы, обращайтесь по номеру 712001110.",
        'en': f"Login to Unired Mobile account " + current_datetime.strftime('%Y-%m-%d %H:%M:%S') + " " + mobile_name + "\nIf this is not you, contact 712001110",
        'uz': f"Unired Mobile akkoutga kirish " + current_datetime.strftime('%Y-%m-%d %H:%M:%S') + " " + mobile_name + "\nAgar bu siz bolmasangiz 712001110 ga murojaat qiling",
    }
    return data[lang]
