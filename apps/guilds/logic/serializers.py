"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.guilds.models import Guild


class GuildSerializer(ModelSerializer):
    """ """

    owner_id = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Guild
        fields = ("id", "name", "owner_id", "description")

    def create(self, validated_data):
        validated_data["owner_id"] = self.context["request"].user
        return super().create(validated_data)
