from v1.gateway import metin_gateway
from v1.models import Users, ClientInfo, AccessToken


def company_staff(user_token, cms):
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
    access_token = AccessToken.objects.select_related('user').get(key=user_token)
    user = access_token.user
    if not user:
        return {
            "message": "User not found",
        }
    user_company = ClientInfo.objects.select_related('user').filter(user=user).first()
    if not user_company:
        return {
            "message": "User is not a director of any company",
        }

    company_staff = Users.objects.filter(workspace=user_company).values('id', 'username', 'first_name', 'last_name',
                                                                        'birth_date', 'phone_number', 'salary')

    for staff in company_staff:
        if 'birth_date' in staff:
            staff['birth_date'] = staff['birth_date'].strftime('%d.%m.%Y')

    return {

        "result": {
            "company": user_company.company_name,
            'staff': list(company_staff)
        }
    }


