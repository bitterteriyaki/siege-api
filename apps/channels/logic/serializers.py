"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import ModelSerializer

from apps.channels.models import Channel
from apps.guilds.logic.utils import get_guild


class ChannelSerializer(ModelSerializer):
    """Serializer for the `/channels` route. This serializer is
    responsible for validating the data sent to the `/channels` route
    and for serializing the data returned by the same route. All of the
    fields are read-only.

    These are the fields that are validated:
    - `name`: must be a string between 1 and 128 characters.
    - `description`: must be a string between 1 and 256 characters.
                     Can be blank.
    """

    class Meta:
        model = Channel
        fields = ("id", "name", "description")

    def create(self, validated_data):
        return Channel.objects.create(
            guild=get_guild(self.context["guild_id"]), **validated_data
        )
