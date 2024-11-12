import datetime
from v1.gateway import egov_gateway, metin_gateway
from v1.models import ClientIABSAccount, Device
from v1.helper.error_messages import MESSAGE


def get_mib_info(user, tin, cms):
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
    # Prepare data
    data = {
        "tin": tin
    }
    # Call the gateway
    result = egov_gateway.egov_info("mib/service/executive-document/v1", data)

    if 'result' in result:
        return {
            'result': result['result']
        }
    if 'error' in result:
        if 'message' in result['error']:
            return {
                "message": result['error']['message']
            }
    return {
        "message": MESSAGE['GovernmentServiceNot']
    }


def get_gas_info(user, tin, cms):
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
    # Prepare data
    data = {
        "tin": tin
    }
    # Call the gateway
    result = egov_gateway.egov_info("hududgaz/service/client/v2/by-tin", data)
    if 'result' in result:
        return {
            'result': result['result']
        }
    if 'error' in result:
        if 'message' in result['error']:
            return {
                "message": result['error']['message']
            }
    return {
        "message": MESSAGE['GovernmentServiceNot']
    }


def get_energy_info(user, endpoint, cms):
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
    # Prepare data
    data = {
        "transaction_id": "123",
        "customer_type": "P",
        "sender_pinfl": "string",
        "purpose": "string",
        "consent": "string",
        "kad_num": "string",
        "soato": "string",
        "licshet": "string",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Call the gateway
    result = egov_gateway.egov_info("res/service/cadastre/v1", data)
    if 'result' in result:
        return {
            'result': result['result']
        }
    if 'error' in result:
        if 'message' in result['error']:
            return {
                "message": result['error']['message']
            }
    return {
        "message": MESSAGE['GovernmentServiceNot']
    }


def get_car_info(user, device_id, cms):
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
    print(device_id)
    device_access = Device.objects.select_related('user').get(user=user, core_id=device_id)
    print(device_access.name)
    if not device_access.verified:
        return {
            "result": {
                "message": "Access denied",
                "status": 401
            }
        }
    client_accounts = ClientIABSAccount.objects.select_related('client').filter(client__user=user).values_list('inn',
                                                                                                               flat=True)
    all_cars_info = []
    processed_tins = set()  # Set to keep track of processed TINs

    for tin in client_accounts:
        if tin in processed_tins:
            continue  # Skip if processed

        data = {"pTin": tin}
        result = egov_gateway.egov_info("yhxbb/service/vehicleinfo/v1/search-by-tin", data)

        if 'result' in result:
            vehicles = result['result'].get('Vehicle', [])
            if isinstance(vehicles, dict):
                vehicles = [vehicles]  # Ensure it's a list

            for vehicle in vehicles:
                car_info = {
                    "vehicle": vehicle,
                    "insurance": None  # Placeholder for insurance data
                }

                iss_data = {"govNumber": vehicle.get('pPlateNumber')}
                insurance_result = egov_gateway.egov_info("insurance/service/policy/v1", iss_data)

                if 'result' in insurance_result:
                    car_info["insurance"] = insurance_result['result'].get('result', [])
                else:
                    car_info["insurance"] = {"error": insurance_result.get('error', 'Unknown error'), "tin": tin}

                all_cars_info.append(car_info)  # Add combined info to the list

        else:
            all_cars_info.append({"error": result.get('error', 'Unknown error'), "tin": tin})

        processed_tins.add(tin)

    return {
        "result": all_cars_info
    }


def get_garbage_info(user, cad_num, time, cms):
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
    # Prepare data
    data = {
        "cad_num": cad_num,
        "time": time
    }
    # Call the gateway
    result = egov_gateway.egov_info("ecology/service/v1/my-home", data)
    if 'result' in result:
        return {
            'result': result['result']
        }
    if 'error' in result:
        if 'message' in result['error']:
            return {
                "message": result['error']['message']
            }
    return {
        "message": MESSAGE['GovernmentServiceNot']
    }
