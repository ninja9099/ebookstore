from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        customized_error_msg = None

        if isinstance(response.data, list):
            customized_error_msg = str(response.data[0])

        elif isinstance(response.data, dict):
            data_keys = response.data.keys()
            if 'detail' in data_keys:
                customized_error_msg = response.data['detail']

            elif 'message' not in data_keys:
                for field, err in response.data.items():
                    break
                customized_error_msg = 'Field (%s): %s' % (field, str(err[0]))

        if customized_error_msg:
            response.data = {
                'message': customized_error_msg,
            }

    return response
