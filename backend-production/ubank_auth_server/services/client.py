from v1.gateway import metin_gateway
from v1.models import DocumentRegistration
from v1.helper.helper import reg_status


def add_client(phone, user_type, pass_front, pass_back, cms, pinfil=None, inn=None, licence=None, order_proxy=None):
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
    documents = DocumentRegistration.objects.filter(phone_number=phone).order_by(
        '-created_at')

    latest_document = documents.first()

    if latest_document and latest_document.status == 0:
        latest_document.status = 1
        latest_document.save()
        return {
            "result": {
                "status": reg_status(latest_document.status)
            }
        }
    elif latest_document and latest_document.status == 1:
        return {
            "result": {
                "status": reg_status(latest_document.status)
            }
        }   
    common_fields = {
        'phone_number': phone,
        'user_type': user_type,
        'passport_front': pass_front,
        'passport_back': pass_back,
    }

    if user_type == 1:
        common_fields.update({
            'tin': inn,
            'licence_certificate': licence,
            'order_proxy': order_proxy
        })
    elif user_type == 2:
        common_fields.update({
            'pinfil': pinfil,
        })
    else:
        return {"message": "Invalid user type"}

    doc = DocumentRegistration.objects.create(**common_fields)
    
    return {
        "result": {
            "Created": True,
            "status": reg_status(doc.status)
        }
    }
