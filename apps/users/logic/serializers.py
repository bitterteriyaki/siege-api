"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any

from django.utils.translation import gettext as _
from rest_framework.serializers import CharField, EmailField, ModelSerializer
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class SelfUserSerializer(ModelSerializer[User]):
    """Serializer for the `/users` route. This serializer is responsible
    for validating the data sent to the `/users` route and for
    serializing the data returned by the same route.

    These are the fields that are validated:
    - `username`: must be a string between 2 and 32 characters long.
    - `password`: must be a string between 8 and 128 characters long.
    - `email`: must be a valid e-mail address.
    - `token`: must be a string between 1 and 255 characters long.
    """

    # Username should have a minimum length of 2 characters and a
    # maximum length of 32 characters.
    username = CharField(min_length=2, max_length=32, write_only=True)

    # The e-mail should be a valid e-mail address and it is also
    # write-only so that it is not returned in the response.
    email = EmailField(
        max_length=255,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_("This email is already in use."),
            )
        ],
    )

    # The password should have a minimum length of 8 characters and a
    # maximum length of 128 characters, and it is also write-only so
    # that it is not returned in the response.
    password = CharField(min_length=8, max_length=128, write_only=True)

    # The user token should be a string with a maximum length of 255
    # characters and it is also read-only so that it is not included
    # in the request.
    token = CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("username", "email", "password", "token")

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class UsersSerializer(ModelSerializer[User]):
    """Serializer for the `/users/<user_id>` route. This serializer is
    responsible for validating the data sent to the `/users/<user_id>`
    route and for serializing the data returned by the same route. All
    of the fields are read-only.

    These are the fields that are validated:
    - `tag`: must be a string between 1 and 4 characters long.
    """

    # The user tag should be a string with a maximum length of 4
    # characters.
    tag = CharField(max_length=4)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "username", "tag", "created_at")
        fields_only_fields = "__all__"
