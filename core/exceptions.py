"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.views import exception_handler

from core.renderers import BaseJSONRenderer


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
    context["request"].accepted_renderer = BaseJSONRenderer()
    response = exception_handler(exc, context)

    error = {"details": response.data, "code": response.status_code}
    response.data = {"error": error}

    return response
