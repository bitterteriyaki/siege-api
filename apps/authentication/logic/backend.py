"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.request import Request

from apps.users.logic.backend import validate_token
from apps.users.models import User


class TokenAuthentication(BaseAuthentication):
    """This class is responsible for authenticating a user using a token
    that is passed in the `Authorization` header of the request.

    The token must be prefixed with `Token` and must be separated from
    the prefix by a space. For example:

    ```
    Authorization: Token <token>
    ```
    """

    header_prefix = "Token"

    def authenticate(self, request: Request) -> tuple[User, str] | None:
        """This method is called on every request, regardless of whether
        the endpoint requires authentication

        This method can return two possible values:

        1) `None` is returned if the request does not contain a valid
        token. In this case, the request will be processed as an
        unauthenticated request.

        2) Tuple[:class:`User`, :class:`str`] is returned when the
        authentication was sucessful. Where this tuple is a pair of
        the user that was authenticated and the token that was used to
        authenticate the user.

        If neither of these two cases were met, that means there was an
        error. In the event of an error, we do not return anything. We
        simple raise the :class:`AuthenticationFailed` exception and let
        Django REST Framework handle the rest.
        """
        auth_header = get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1 or len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix != self.header_prefix:
            return None

        return validate_token(token)

    def authenticate_header(self, request: Request) -> str:
        """This method is called when the client does not provide a
        valid token in the `Authorization` header of the request.

        This method returns a string that is sent to the client as the
        value of the `WWW-Authenticate` header. This header tells the
        client what type of authentication is required and how to
        authenticate.
        """
        return self.header_prefix
