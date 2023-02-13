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
    """Serializer responsible to return sensitive data about the user,
    this is only used to return the user token when the user is creating
    a new account. Also, when the user is creating a new account, they
    must provide an username, an e-mail and a password. The token is
    returned in the response.
    """

    # Username should have a minimum length of 2 characters and a
    # maximum length of 32 characters. This is a write-only field so
    # that it is not returned in the response.
    username = CharField(min_length=2, max_length=32, write_only=True)

    # The e-mail should be a valid e-mail address and it is also
    # write-only so that it is not returned in the response. This field
    # also has a unique validator so that no two users can have the same
    # e-mail address.
    email = EmailField(
        max_length=256,
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

    # The token is a string between 1 and 255 characters long and it is
    # read-only so that it must not be provided in the request.
    token = CharField(max_length=256, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("username", "email", "password", "token")

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class UserSerializer(ModelSerializer[User]):
    """This serializer is responsible to return the user schema, this
    must not return sensitive data like the user token. This is used
    to represent an user in the response.
    """

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "username", "tag", "created_at")
        read_only_fields = fields

    def to_representation(self, instance: User) -> Any:
        representation = super().to_representation(instance)
        # Fill the tag with zeros to the left so that it has a length
        # of 4 characters.
        representation["tag"] = str(instance.tag).zfill(4)
        return representation
