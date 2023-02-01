"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.guilds.models import Guild
from apps.members.logic.serializers import MemberSerializer


class GuildSerializer(ModelSerializer):
    """Serializer for the `/guilds` route. This serializer is
    responsible for validating the data sent to the `/guilds` route
    and for serializing the data returned by the same route. This
    serializer also handles the creation of guilds.

    These are the fields that are validated:
    - `name`: must be a string between 1 and 128 characters long.
    - `description`: must be a string between 0 and 255 characters.
    """

    owner_id = PrimaryKeyRelatedField(read_only=True)
    members = MemberSerializer(
        many=True, read_only=True, source="guildmember_set"
    )

    class Meta:
        model = Guild
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "name", "owner_id", "description", "members")

    def create(self, validated_data):
        validated_data["owner_id"] = self.context["request"].user
        return super().create(validated_data)
