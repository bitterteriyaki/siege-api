"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any, cast

from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotAuthenticated
from rest_framework.serializers import CharField, EmailField, Serializer

from apps.users.models import User


class LoginSerializer(Serializer[Any]):
    """ """

    email = EmailField(max_length=256, write_only=True, required=True)
    password = CharField(max_length=128, write_only=True, required=True)
    token = CharField(max_length=256, read_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        email = attrs["email"]
        password = attrs["password"]

        user = cast(User, authenticate(username=email, password=password))

        if user is None or not user.is_active:
            raise NotAuthenticated(
                _("Unable to log in with provided credentials.")
            )

        return {"token": user.token}
