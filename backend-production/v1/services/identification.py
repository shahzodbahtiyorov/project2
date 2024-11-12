#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import sys
from datetime import time
from django.db.models import Q
import requests

from datetime import datetime, timedelta

from v1.gateway import metin_gateway
from v1.helper.error_messages import MESSAGE
from v1.models import Identification, Card
from v1.models.users import Users, AccessToken
from v1 import MY_ID_GRANT_TYPE, MY_ID_URL, MY_ID_CLIENT_ID, MY_ID_CLIENT_SECRET_KEY

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def my_id_identification_create(user, code, image, cms, unired=None):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }
    current_datetime = datetime.now()

    start_time = time(17, 0, 0)
    end_time = time(4, 0, 0)

    start_datetime = datetime.combine(current_datetime.date(), start_time)
    end_datetime = datetime.combine(current_datetime.date(), end_time)

    if start_datetime > current_datetime and current_datetime < end_datetime:
        return {
            "message": MESSAGE['ForbiddenIdentification']
        }

    identification = Identification.objects.filter(user=user, is_deleted=False).first()
    if identification:
        return {
            'message': MESSAGE['HasIdentification']
        }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = f'grant_type={MY_ID_GRANT_TYPE}&code={code}&client_id={MY_ID_CLIENT_ID}&client_secret={MY_ID_CLIENT_SECRET_KEY}'
    endpoint = 'api/v1/oauth2/access-token'
    try:
        response = requests.post(MY_ID_URL + endpoint, headers=headers, data=payload)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return {
            'message': f"Request failed: {str(e)}"
        }
    except ValueError:
        return {
            'message': f"Invalid JSON response: {response.text}"
        }

    if 'access_token' in response_data:
        identification = Identification(
            user=user,
            code=code,
            image=image,
            access_token=response_data['access_token'],
            expires_in=response_data['expires_in'],
            token_type=response_data['token_type'],
            scope=response_data['scope'],
            refresh_token=response_data['refresh_token'],
            comparison_value=response_data['comparison_value']
        )
        identification.save()

        endpoint = 'api/v1/users/me'
        headers = {
            'Authorization': f'Bearer {identification.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(MY_ID_URL + endpoint, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            return {
                'message': f"Profile request failed: {str(e)}"
            }
        except ValueError:
            return {
                'message': f"Invalid JSON response from profile request: {response.text}"
            }

        if 'profile' in response_data:
            # Update identification record with profile data
            identification.seria = response_data['profile']['doc_data']['pass_data']
            identification.pinfl = response_data['profile']['common_data']['pinfl']
            identification.response = response_data
            identification.must_refresh_token = identification.created_at
            identification.save()

            pinfil = Identification.objects.filter(pinfl=identification.pinfl, is_deleted=False)
            if len(pinfil) > 1:
                identification.delete()
                return {
                    'message': MESSAGE['HasIdentification']
                }
            if identification.pinfl == '51405065220031':
                identification.delete()
                return {
                    'message': MESSAGE['PermissionDenied']
                }

            name = f"{response_data['profile']['common_data']['first_name']} {response_data['profile']['common_data']['last_name']}"
            cards = Card.objects.filter(user=user, type__in=[0, 1]).all()
            for card in cards:
                card.is_verified = 1
                card.save()

            cards = Card.objects.filter(user=user, type__in=[19, 20]).all()
            for card in cards:
                card.name = name
                card.card_owner = name
                card.save()

            return {
                "result": {
                    "access": True
                }
            }

        return {
            'message': response_data
        }

    return {
        'message': response_data
    }


def my_id_user_info(user, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }
    identification = Identification.objects.filter(user=user).first()
    if not identification:
        return {
            'message': MESSAGE['identification']
        }
    return {
        "result": {
            "type": 'auto',
            "profile": identification.response['profile']
        }
    }


def my_id_check_seria(user: Users, seria, birthday):
    current_datetime = datetime.now()

    # Define the start and end times for your range
    start_time = time(17, 0, 0)  # 22:00:00
    end_time = time(4, 0, 0)  # 09:00:00

    # Create datetime objects for the start and end times using today's date
    start_datetime = datetime.combine(current_datetime.date(), start_time)
    end_datetime = datetime.combine(current_datetime.date(), end_time)
    if start_datetime > current_datetime and current_datetime < end_datetime:
        return {
            "message": MESSAGE['ForbiddenIdentification']
        }
    identification = Identification.objects.filter(Q(seria=seria) | Q(pinfl=seria), is_deleted=False).first()
    if identification:
        return {
            'message': MESSAGE['HasIdentification']
        }
    return {
        "result": {
            "seria": seria,
            "birthday": birthday
        }
    }


def my_id_identification_delete(user):
    identification = Identification.objects.filter(user=user).first()
    if identification:
        identification.delete()
        return {
            "result": {
                "access": True
            }
        }
    return {
        'message': MESSAGE['NotData']
    }
