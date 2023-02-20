"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.guilds.models import Guild
from apps.users.models import User

if TYPE_CHECKING:
    GuildOwnerField = PrimaryKeyRelatedField[User]
else:
    GuildOwnerField = PrimaryKeyRelatedField


class GuildSerializer(ModelSerializer[Guild]):
    """This serializer is responsible to return the user schema. This is
    used to represent the guild in the response.
    """

    owner_id = GuildOwnerField(read_only=True)

    class Meta:
        model = Guild
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "name", "description", "owner_id")

    def create(self, validated_data: dict[str, str]) -> Guild:
        # The owner of the guild is the user who is making the request.
        validated_data["owner_id"] = self.context["request"].user
        return super().create(validated_data)
