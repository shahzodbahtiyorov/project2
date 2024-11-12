import uuid
from datetime import datetime

from v1.helper import helper, card_logo, bank_logo, card_background, card_type
from v1.helper.comparation import compare_fio
from v1.helper.helper import check_otp_add_card
from v1.models import Users, Card
from v1.helper.logger import Logger
from v1.gateway import uzcard_gateway, humo_gateway
from v1.helper.error_messages import MESSAGE

logger = Logger(__name__, False, 10)


def register_uzcard_one(user_id: int, card_number, expire, lang):
    user = Users.objects.get(id=user_id)
    sms = False
    print(user)
    identification = user.identification.first()
    print(identification)
    if not identification:
        return {
            "message": MESSAGE['NotIdentification']
        }
    identify = 1
    data = {
        'number': card_number,
        'expire': expire
    }
    result = uzcard_gateway.post('api/v1/unired/', 'card.new.otp', data)
    log = {
        'data': data,
        'result': result,
    }
    logger.info(log)
    if 'result' in result:
        return {
            'result': {
                'otp_token': str(result['result']['ext_id']),
                'card': str(result['result']['ext_id']),
                "count": 6
            }
        }
    if 'error' in result:
        return {
            "message": result['error']['message']
        }
    return {
        "message": MESSAGE['UzCardServiceNot']
    }


def register_uzcard_two(user_id: int, name, card_number, expire, primary, otp, otp_token, card_id):
    user = Users.objects.get(id=user_id)
    logger.info(card_number + ' ' + card_id + '___' + otp + '___' + otp_token)
    data = {
        'ext_id': otp_token,
        'code': otp
    }
    result = uzcard_gateway.post('api/v1/unired/', 'card.new.verify', data)
    log = {
        'data': data,
        'result': result,
    }
    logger.info(log)
    if 'error' in result:
        return {
            "message": result['error']['message']
        }
    identification = user.identification.first()

    if not identification:
        return {
            "message": MESSAGE['NotIdentification']
        }
    identify = 1
    if 'result' in result:
        if not result['result']['sms']:
            return {
                "message": MESSAGE['card_sms']
            }
        if result['result']['cardtype'] == 'corporate':
            return {
                "message": MESSAGE['corporate_card']
            }
        if '998' + result['result']['phone'][-9:] != user.username:
            return {
                "message": MESSAGE['PhoneAndCardPhoneError']
            }
        if result["result"]["status"] != 0:
            return {
                "message": MESSAGE["CardIsBlocked"]
            }
        card = Card.objects.filter(token=result['result']['id'], user=user).first()
        is_unired = 0
        if card_number[0:8] == '86004888':
            is_unired = 1
        if card:
            card.name = name
            card.is_primary = primary
            if identify:
                card.balance = result['result']['balance']
            else:
                card.balance = 0
            card.card_registered_phone = result['result']['phone']
            card.is_verified = identify
            card.is_unired = is_unired
            card.save()
            return {
                "result": card.collection()
            }
        else:
            response = identification.response
            middle_name = response['profile']['common_data']['middle_name']
            if response['profile']['common_data']['first_name'] and response['profile']['common_data'][
                'last_name']:
                firstname = response['profile']['common_data']['first_name']
                lastname = response['profile']['common_data']['last_name']

            else:
                firstname = response['profile']['common_data']['first_name_en']
                lastname = response['profile']['common_data']['last_name_en']
            fio1 = firstname + ' ' + lastname
            fio2 = firstname + ' ' + lastname + ' ' + middle_name
            compare1 = compare_fio(user, fio1, result['result']['fullName'])
            compare2 = compare_fio(user, fio2, result['result']['fullName'])
            if compare1 < 50:
                logger.info('compare1 ---' + user.username + '---' + fio1 + '---' + result['result']['fullName'])
                if compare2 < 50:
                    logger.info(
                        'compare2 ---' + user.username + '---' + fio2 + '---' + result['result']['fullName'])
                    if lastname in result['result']['fullName']:
                        logger.info(
                            'compare3 ---' + user.username + '---' + fio1 + '---' + result['result']['fullName'])
                    else:
                        if firstname in result['result']['fullName']:
                            logger.info(
                                'compare4 ---' + user.username + '---' + fio1 + '---' + result['result'][
                                    'fullName'])
                        else:
                            logger.info(
                                'compare5 ---' + user.username + '---' + fio1 + '---' + result['result'][
                                    'fullName'])
                            return {
                                "message": MESSAGE['AddCardDeny']
                            }
                logger.info('compare1_ ---' + user.username + '---' + fio1 + '---' + result['result']['fullName'])

            card = Card()
            card.user = user
            card.name = name
            if identify:
                card.balance = result['result']['balance']
            else:
                card.balance = 0
            card.number = card_number
            card.mask = helper.card_mask(card_number)
            card.token = result['result']['id']
            card.expire = expire
            card.card_owner = result['result']['fullName']
            card.card_logo = card_logo.get_logo(0)
            card.bank_logo = bank_logo.get_logo(card_number)
            card.bank_background = card_background.get_background(card_number)
            card.is_unired = is_unired
            card.is_primary = primary
            card.is_verified = identify
            card.card_registered_phone = result['result']['phone']
            card.is_salary = 0
            card.type = card_type.UZCARD
            card.blocked = 0
            card.save()

        return {
            "result": card.collection()
        }
    if 'error' in result:
        return {
            "message": result['error']['message']
        }
    return {
        "message": MESSAGE['UzCardServiceNot']
    }


def register_humo_one(user_id: int, card_number, expire, lang):
    user = Users.objects.get(id=user_id)
    identification = user.identification.first()
    if not identification:
        return {
            "message": MESSAGE['NotIdentification']
        }
    identify = 1

    data = {
        'card_number': card_number,
        'expire': expire
    }
    result = humo_gateway.post('api/v1/', 'register.card', data)
    logger.info(result)
    if 'result' in result:
        data = {
            'token': result['result']['token']
        }
        result = humo_gateway.post('api/v1/', 'get.card', data)
        logger.info(result)
        if 'result' in result:
            if not result['result']['sms']:
                return {
                    "message": MESSAGE['card_sms']
                }
            if result['result']['is_corporate']:
                return {
                    "message": MESSAGE['corporate_card']
                }
            if result['result']['state'] != 0 and result['result']['status'] != 0:
                return {
                    "message": MESSAGE['CardIsBlocked']
                }
            phone = result['result']['phone']
            if '998' + phone[-9:] != user.username:
                return {
                    "message": MESSAGE['PhoneAndCardPhoneError']
                }
            sms = False
            card_id = False
            if not user.is_sms:
                card_id = 'U_M_C_A_' + f"{uuid.uuid4()}"
                sms = helper.sms_sender_add_card(user.username, lang, helper.card_mask(card_number), card_id)
            return {
                'result': {
                    'otp_token': sms,
                    'card': card_id,
                    "count": 5
                }
            }

        if 'error' in result:
            return {
                "message": result['error']['message']
            }
        return {
            "message": MESSAGE['HumoServiceNot']
        }
    if 'error' in result:
        return {
            "message": result['error']['message']
        }
    return {
        "message": MESSAGE['HumoServiceNot']
    }


def register_humo_two(user_id: int, name, card_number, expire, primary, otp, otp_token, card_id):
    user = Users.objects.get(id=user_id)
    logger.info(card_number + ' ' + card_id + '___' + otp + '___' + otp_token)
    if not user.is_sms:
        result = check_otp_add_card(user.username, otp, otp_token, card_id, helper.card_mask(card_number))
        if 'message' in result:
            return {
                "message": result['message']
            }
    identification = user.identification.first()
    if not identification:
        return {
            "message": MESSAGE['NotIdentification']
        }
    identify = 1

    data = {
        'card_number': card_number,
        'expire': expire
    }
    result = humo_gateway.post('api/v1/', 'register.card', data)
    log = {
        'data': data,
        'result': result,
    }
    logger.info(log)
    if 'result' in result:
        data = {
            'token': result['result']['token']
        }
        result = humo_gateway.post('api/v1/', 'get.card', data)
        log = {
            'data': data,
            'result': result,
        }
        logger.info(log)
        if 'result' in result:
            if not result['result']['sms']:
                return {
                    "message": MESSAGE['card_sms']
                }
            if result['result']['is_corporate']:
                return {
                    "message": MESSAGE['corporate_card']
                }
            if result['result']['state'] != 0 and result['result']['status'] != 0:
                return {
                    "message": MESSAGE['CardIsBlocked']
                }
            phone = result['result']['phone']
            if '998' + phone[-9:] != user.username:
                return {
                    "message": MESSAGE['PhoneAndCardPhoneError']
                }
            card = Card.objects.filter(token=data['token'], user=user).first()
            if card:
                card.name = name
                card.is_primary = primary
                if identify:
                    card.balance = result['result']['balance']
                else:
                    card.balance = 0
                card.card_registered_phone = phone[1:]
                card.is_verified = identify
                card.save()
                return {
                    "result": card.collection()
                }
            else:
                response = identification.response
                middle_name = response['profile']['common_data']['middle_name']
                if response['profile']['common_data']['first_name'] and response['profile']['common_data']['last_name']:
                    firstname = response['profile']['common_data']['first_name']
                    lastname = response['profile']['common_data']['last_name']

                else:
                    firstname = response['profile']['common_data']['first_name_en']
                    lastname = response['profile']['common_data']['last_name_en']
                fio1 = firstname + ' ' + lastname
                fio2 = firstname + ' ' + lastname + ' ' + middle_name
                compare1 = compare_fio(user, fio1, result['result']['owner'])
                compare2 = compare_fio(user, fio2, result['result']['owner'])
                if compare1 < 50:
                    logger.info('compare1 ---' + user.username + '---' + fio1 + '---' + result['result']['owner'])
                    if compare2 < 50:
                        logger.info('compare2 ---' + user.username + '---' + fio2 + '---' + result['result']['owner'])
                        if lastname in result['result']['owner']:
                            logger.info(
                                'compare3 ---' + user.username + '---' + fio1 + '---' + result['result']['owner'])
                        else:
                            if firstname in result['result']['owner']:
                                logger.info(
                                    'compare4 ---' + user.username + '---' + fio1 + '---' + result['result'][
                                        'owner'])
                            else:
                                logger.info(
                                    'compare4 ---' + user.username + '---' + fio1 + '---' + result['result'][
                                        'owner'])
                                return {
                                    "message": MESSAGE['AddCardDeny']
                                }
                    logger.info('compare1_ ---' + user.username + '---' + fio1 + '---' + result['result']['owner'])

                card = Card()
                card.user = user
                card.name = name
                if identify:
                    card.balance = result['result']['balance']
                else:
                    card.balance = 0
                card.number = card_number
                card.mask = helper.card_mask(card_number)
                card.token = data['token']
                card.expire = result['result']['expire']
                card.card_owner = result['result']['owner']
                card.card_logo = card_logo.get_logo(1)
                card.bank_logo = bank_logo.get_logo(card_number)
                card.bank_background = card_background.get_background(card_number)
                card.is_unired = 0
                card.is_primary = primary
                card.is_verified = identify
                card.card_registered_phone = phone[1:]
                card.is_salary = 0
                card.type = 1
                card.blocked = 0
                card.save()

            return {
                "result": card.collection()
            }
        if 'error' in result:
            return {
                "message": result['error']['message']
            }
        return {
            "message": MESSAGE['HumoServiceNot']
        }
    if 'error' in result:
        return {
            "message": result['error']['message']
        }
    return {
        "message": MESSAGE['HumoServiceNot']
    }
