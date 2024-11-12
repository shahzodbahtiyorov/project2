from jsonrpcserver import Error, Success


def response_handler(response):
    if 'result' in response:
        return Success(response['result'])
    if 'error' in response:
        code = response['error']['code']
        message = response['error']['message']
        return Error(code, message)
    else:
        code = 999
        message = response
        if 'code' in response:
            code = response['code']
        if 'message' in response:
            message = response['message']

        return Error(code, message)
