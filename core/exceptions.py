from rest_framework.views import exception_handler


def main_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    response.data = {"errors": response.data}
    return response
