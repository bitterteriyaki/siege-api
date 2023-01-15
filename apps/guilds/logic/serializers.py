"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import (
    DateTimeField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from apps.guilds.models import Guild, GuildMember
from apps.users.logic.serializers import UsersSerializer


class GuildMemberSerializer(ModelSerializer):
    """Serializer for the `/guilds/<guild_id>/members` route. This
    serializer is responsible for validating the data sent to the route
    and for serializing the data returned by the same route. This
    serializer also handles the creation of guild members.
    """

    user = SerializerMethodField()
    joined_at = DateTimeField(read_only=True)

    class Meta:
        model = GuildMember
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("nick", "user", "joined_at")
        fields_read_only = "__all__"

    def get_user(self, member):
        return UsersSerializer(member.user).data


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
    members = GuildMemberSerializer(
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
