"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.members.models import Member
from apps.users.logic.serializers import UserSerializer


class MemberSerializer(ModelSerializer):
    """Serializer for the `/guilds/<guild_id>/members` route. This
    serializer is responsible for validating the data sent to the route
    and for serializing the data returned by the same route. This
    serializer also handles the creation of guild members.
    """

    user = SerializerMethodField()

    class Meta:
        model = Member
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("nick", "user", "joined_at")
        fields_read_only = "__all__"

    def get_user(self, member):
        return UserSerializer(member.user).data
