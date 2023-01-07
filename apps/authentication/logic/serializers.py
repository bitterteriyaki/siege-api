"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)


class AuthenticationSerializer(Serializer):
    """Serializer for the `/auth/login` route. This serializer is
    responsible for validating the data sent to the route and
    serializing the data returned by the same route.

    The are the fields that are validated:
    - `email`: must be a valid e-mail address.
    - `password`: must be a string between 8 and 128 characters long.
    """

    # The e-mail address should be a valid e-mail address.
    email = EmailField(max_length=255, write_only=True)

    # The password should have a minimum length of 8 characters and a
    # maximum length of 128 characters, and it is also write-only so
    # that it is not returned in the response.
    password = CharField(max_length=128, write_only=True)

    # The user token should be a string with a maximum length of 255
    # characters and it is also read-only so that it is not included
    # in the request.
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise ValidationError("An e-mail address is required to login.")

        if password is None:
            raise ValidationError("A password is required to login.")

        user = authenticate(username=email, password=password)

        if user is None or not user.is_active:
            raise PermissionDenied(
                "Unable to login with provided credentials."
            )

        return {
            "email": user.email,
            "username": user.username,
            "token": user.token,
        }
