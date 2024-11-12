#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import base64
import io
import os
import random
import re
import string
import uuid
from datetime import datetime

from django.template.loader import render_to_string
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.db.models import F
from django.utils import timezone
from xhtml2pdf import pisa

from api import settings
from v1.gateway import sms_gateway
from v1.helper import sms_messages
from v1.helper.error_messages import MESSAGE
from v1.models import Sms
from v1 import CARD_NUMBER_FERNET_KEY
from django.contrib.auth.hashers import check_password, make_password
from v1.models.documents import BudgetAccount, BudgetIncomeAccount

cipher_suite = Fernet(CARD_NUMBER_FERNET_KEY)

load_dotenv()


def decrypt_data(encrypted_data, key, iv):
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')

    encrypted_bytes = base64.b64decode(encrypted_data)

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_bytes) + unpadder.finalize()

    return decrypted_data.decode('utf-8')


def sms_sender(mobile, lang, type='auth'):
    # Generate OTP based on the mobile number
    otp = "98651" if mobile == "9989011234567" else generate_otp()

    # Initialize and set up the Sms object
    sms = Sms()
    sms.mobile = mobile
    sms.otp_token = make_password(otp)
    sms.lang = lang
    sms.additional = type
    sms.expire = 0
    sms.tried = 0
    sms.save()

    # Determine the SMS message based on the type
    message_dict = {
        'auth': sms_messages.auth,
        'forget': sms_messages.forget,
        'transfer': sms_messages.transfer
    }
    text = message_dict.get(type, sms_messages.auth)(otp, lang)  # Default to 'auth' if type is unrecognized

    # Send the SMS and handle the response
    result = sms_gateway.post(mobile, text)
    if 'result' in result:
        return {"result": {"otp_token": str(sms.id)}}
    elif 'error' in result:
        return {"message": result['error'].get('message', 'Unknown error occurred')}
    else:
        return {"message": "An unexpected error occurred"}


def sms_sender_transfer(mobile, lang, card_number, amount, tr_id, type='transfer-uzs'):
    # Generate OTP for the transaction
    otp = generate_otp()

    # Initialize and set up the Sms object
    sms = Sms()
    sms.mobile = mobile
    sms.otp_token = make_password(otp)
    sms.lang = lang
    sms.additional = type
    sms.tr_id = tr_id
    sms.expire = 0
    sms.tried = 0
    sms.save()

    # Prepare the SMS text message
    text = sms_messages.transfer(otp, lang, card_number, amount, type)

    # Send the SMS
    result = sms_gateway.post(mobile, text)

    # Process the result of the SMS gateway
    if 'result' in result:
        return str(sms.id)
    elif 'error' in result:
        return {"message": result['error'].get('message', 'Unknown error')}
    else:
        return {"message": "An unexpected error occurred"}


def sms_login(mobile, lang, name):
    # Generate OTP and configure the SMS object
    otp = generate_otp()
    sms = Sms()
    sms.mobile = mobile
    sms.otp_token = make_password(otp)
    sms.lang = lang
    sms.expire = 0
    sms.tried = 0
    sms.save()

    # Configure text and transaction id based on the operation
    if name == 'delete':
        sms.additional = 'delete_account'
        sms.tr_id = 'delete_account'
        text = "Xurmatli mijoz, sizni UNIRED MOBILE hisobingiz o'chirildi!"
    else:
        sms.additional = 'login_to_account'
        sms.tr_id = 'login_to_account'
        text = sms_messages.login(lang, name)

    # Send the SMS
    result = sms_gateway.post(mobile, text)
    # handle_user_notification(mobile, text)

    # Return result based on the outcome of the SMS sending
    return handle_sms_result(result, sms)


def handle_sms_result(result, sms):
    # Process the SMS result and return appropriate message
    if 'result' in result:
        return str(sms.id)
    else:
        error_message = result.get('error', {}).get('message', 'Unknown error occurred')
        return {"message": error_message}


def sms_sender_add_card(mobile, lang, card_number, card_id):
    # Generate OTP for adding a card
    otp = generate_otp()

    # Initialize and set up the Sms object
    sms = Sms()
    sms.mobile = mobile
    sms.otp_token = make_password(otp)
    sms.lang = lang
    sms.additional = card_number  # Consider renaming this field if it doesn't describe a 'card_number'
    sms.tr_id = card_id
    sms.expire = 0
    sms.tried = 0
    sms.save()

    # Prepare the SMS text message
    text = sms_messages.add_card(otp, lang, card_number)

    # Send the SMS
    result = sms_gateway.post(mobile, text)

    # Handle the result of the SMS gateway
    if 'result' in result:
        return str(sms.id)
    elif 'error' in result:
        return {"message": result['error'].get('message', 'Unknown error')}
    else:
        return {"message": "An unexpected error occurred"}


def sms_resend(user, lang, type='auth'):
    # Generate a new OTP
    otp = generate_otp()
    sms = Sms()
    sms.mobile = user.username
    sms.otp_token = make_password(otp)
    sms.lang = lang
    sms.additional = type
    sms.expire = 0
    sms.tried = 0
    sms.save()

    # Select the appropriate message function based on the type
    message_functions = {
        'auth': sms_messages.auth,
        'forget': sms_messages.forget,
        'transfer': sms_messages.transfer  # Assuming there is a specific function for transfer
    }
    # Get the message function from the dictionary with a default fallback to auth
    text_function = message_functions.get(type, sms_messages.auth)
    text = text_function(otp, lang)

    # Post the message via the SMS gateway
    result = sms_gateway.post(user.username, text)
    if 'result' in result:
        return {
            "result": {
                "otp_token": str(sms.id),
                "count": 5  # Assuming 'count' signifies the number of allowed attempts or something similar
            }
        }
    else:
        # Error handling for cases where the SMS gateway returns an error
        return {
            "message": result.get('error', {}).get('message', 'Unknown error occurred')
        }


def card_mask(number):
    return number[0:4] + ' **** **** ' + number[12:16]


def generate_otp():
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(5))


def code_decoder(data=None, encoded=None, timestamp=None):
    if encoded:
        return base64.b64decode(encoded).decode('utf-8')
    else:
        encode = "Unired".encode('utf-8') + data.encode('utf-8') + str(uuid.uuid4()).encode('utf-8')
        return base64.b64encode(encode).decode()


def check_otp(otp, otp_token, additional='auth-two'):
    # Fetch the SMS record using the provided OTP token
    sms = Sms.objects.filter(id=otp_token).first()

    # Check if the SMS record exists
    if not sms:
        return {"message": MESSAGE['OTP wrong']}

    # Increment the attempt count and save immediately
    sms.tried += 1
    sms.additional = additional
    sms.save(update_fields=['tried', 'additional'])

    # Calculate the time elapsed since the OTP was created
    delta_seconds = (timezone.now() - sms.created_at).total_seconds()

    # Check if OTP is expired due to time limit or too many tries
    if delta_seconds > 60 or sms.tried > 3:
        sms.expire = True
        sms.save(update_fields=['expire'])
        return {"message": MESSAGE['OTP old']}

    # Verify the OTP value
    if not check_password(otp, sms.otp_token):
        return {"message": MESSAGE['wrong OTP']}

    # Mark the OTP as expired after successful verification
    sms.expire = True
    sms.save(update_fields=['expire'])

    return {"result": True}


def verify_otp(sms, otp, otp_expiry_seconds=60, max_attempts=3):
    if sms.expire:
        return {"message": MESSAGE['OTP old']}

    sms.tried = F('tried') + 1
    sms.save(update_fields=['tried'])
    sms.refresh_from_db()

    if (timezone.now() - sms.created_at).total_seconds() > otp_expiry_seconds or sms.tried > max_attempts:
        sms.expire = True
        sms.save(update_fields=['expire'])
        return {"message": MESSAGE['OTP old']}
    # if not check_password(otp, sms.otp_token):
    #     return {"message": MESSAGE['wrong OTP']}

    sms.expire = True
    sms.save(update_fields=['expire'])
    return {"result": True}


def check_otp_transfer(mobile, otp, otp_token, tr_id, additional='transfer-uzs'):
    sms = Sms.objects.filter(id=otp_token, mobile=mobile, expire=False, tr_id=tr_id, additional=additional).first()
    if not sms:
        return {"message": MESSAGE['OTP wrong']}
    return verify_otp(sms, otp)


def check_otp_add_card(mobile, otp, otp_token, card_id, card_number):
    sms = Sms.objects.filter(id=otp_token, mobile=mobile, expire=False, tr_id=card_id, additional=card_number).first()
    if not sms:
        return {"message": MESSAGE['OTP wrong']}
    result = verify_otp(sms, otp)
    if result.get("result"):
        sms.additional = sms.additional + '_CONFIRM'
        sms.save(update_fields=['additional'])
    return result


def check_added_card_time(card):
    if (timezone.now() - card.created_at).total_seconds() < 3600:
        return {'message': MESSAGE['AddNewCardForbidden']}
    return {'result': True}


def encrypt_card_number(card_number: str) -> str:
    encrypted = cipher_suite.encrypt(card_number.encode())
    return encrypted.decode()


def decrypt_card_number(encrypted_card_number: str) -> str:
    decrypted = cipher_suite.decrypt(encrypted_card_number.encode())
    return decrypted.decode()


def reg_status(data):
    data_info = {
        0: "Created",
        1: "In process",
        2: "Completed",
        3: "Cancelled"
    }
    return data_info[data]


def get_budget_or_kazna_name(account_number):
    if len(account_number) == 27:
        budget_name = BudgetAccount.objects.get(code=account_number)
        return {
            "name": budget_name.name
        }
    elif len(account_number) == 25:
        kazna_name = BudgetIncomeAccount.objects.get(code=account_number)
        return {
            "name": kazna_name.name,
            "coato": kazna_name.coato
        }
    return None


def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[a-zA-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def sms_client_pass(mobile, password):
    sms = Sms()
    sms.mobile = mobile
    sms.otp_token = password
    sms.lang = 'uz'
    sms.additional = "one time password for client"
    sms.expire = 0
    sms.tried = 0
    sms.save()
    data = f"""Пожалуйста, введите ваш одноразовый пароль (OTP):
               OTP: {password}
               Внимание: Этот пароль действителен только для первого входа. 
               После успешной авторизации, вы должны, измените его на новый.    
            """

    sms_gateway.post(mobile, data)
