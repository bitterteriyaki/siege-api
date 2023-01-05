"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.views import exception_handler


def main_exception_handler(exc, context):
    """A custom exception handler that returns errors in a format that
    is consistent with the rest of the API. The response will include
    a `status_code` key that will contain the HTTP status code of the
    response and an `errors` key that will contain the errors that
    were raised.

    Parameters
    ----------
    exc: :class:`Exception`
        The exception that was raised.
    context: Dict[:class:`str`, Any]
        The context of the exception.
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    response.data = {"errors": response.data}
    return response
