from v1.models import Users, AccessToken, Device
from v1.models.client import ClientInfo, ClientCertificate
from v1.gateway import bot_gateway, metin_gateway
from v1.helper.helper import is_valid_password


def user_login(username, password, certificate, device_info):
    print(device_info)
    core_id = device_info['core_id']
    ip = device_info['ip']
    uid = device_info['uid']
    reg_id = device_info['reg_id']
    name = device_info['name']
    version = device_info['version']
    user = Users.objects.filter(username=username).first()
    device = Device.objects.select_related('user').filter(core_id=core_id).first()
    if not user:
        return {
            "message": "Incorrect username or password",
        }
    if device.is_blocked:
        return {
            "result": {
                "message": "Your device is blocked",
            }
        }
    if not user.check_password(password):
        device.tries += 1
        device.save()
        return {
            "message": "Incorrect username or password",
        }

    if device:
        if device.user != user:
            return {
                "message": "This device does not belong to the current client",
            }

        device.firebase_reg_id = reg_id
        device.ip = ip
        device.save()

        if not device.verified:
            return {
                "message": "Your device is not verified",
            }
    else:
        device = Device.objects.create(
            user=user,
            core_id=core_id,
            uuid=uid,
            ip=ip,
            name=name,
            firebase_reg_id=reg_id,
            version=version
        )
        message = f"📱New device created:\n👤Username: {device.user}\n⚙️Device: {device.name}\n🔗Approval link: Link from dashboard"
        bot_gateway.send_telegram_message(message)

    access_token = AccessToken.objects.filter(user_id=user.id).first()
    if not device.verified:
        return {
            "message": "Your device is not verified",
        }

    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    client_cert = ClientCertificate.objects.select_related('client').filter(client=client).first()

    return {
        "result": {
            "address": client.address,
            "common_name": user.username,
            "country": client.country,
            "email": user.email,
            "locality": client.locality,
            "org": client.client_name,
            "org_unit": client.org_unit,
            "otp_code": client_cert.otp_code,
            "phone_number": user.phone_number,
            "state": client.state,
            "pin_code": client_cert.pin_code,
            "inn": client.tin,
            "has_password": client.has_password,
            "user_token": access_token.key,
        }
    }


def change_password(user, current_password, new_password, cms):
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
    username = user.username
    user = Users.objects.filter(username=username).first()

    if not user.check_password(current_password):
        return {
            "result": {
                "message": "Incorrect current password",
                "status": 1
            }
        }

    if current_password == new_password:
        return {
            "result": {
                "message": "Current password is same as new password",
                "status": 2
            }}
    if not is_valid_password(new_password):
        return {
            "result": {
                "message": "New password should contain at least one capital letter, one symbol, one number, minimal length 8",
                "status": 3
            }
        }
    user.set_password(new_password)
    user.save()

    return {
        "result": {
            "message": "Password changed successfully",
            "status": 0
        }}


def get_cert_codes(user, otp_code, pin_code):
    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    if not client:
        return {
            "result": {
                "msg": "client not found"
            }
        }

    cert_data = ClientCertificate.objects.select_related('client').filter(client=client).first()
    cert_data.pin_code = pin_code
    cert_data.otp_code = otp_code
    cert_data.save()

    return {
        "result": {
            "otp_code": cert_data.otp_code,
            "pin_code": cert_data.pin_code,
        }
    }


def get_cert_cms(user, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)

    return {
        "result": {
            "status": response['status'],
            "message": response['message'],
            "is_revoked": response['revokeStatus'],
        }
    }


def change_mandatory_password(user, new_password):
    user = Users.objects.filter(username=user.username).first()
    client = ClientInfo.objects.select_related('user').filter(user=user).first()
    if not is_valid_password(new_password):
        return {
            "result": {
                "message": "New password should contain at least one capital letter, one symbol, one number, minimal length 8",
                "status": 3
            }
        }
    user.set_password(new_password)
    user.save()
    client.has_password = True
    client.save()
    return {
        "result": {
            "success": client.has_password,
        }
    }
