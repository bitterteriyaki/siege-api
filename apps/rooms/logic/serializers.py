"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from apps.rooms.models import Room, RoomRecipient
from apps.users.logic.serializers import UserSerializer
from apps.users.models import User


class RoomSerializer(ModelSerializer[Room]):
    """Serializer responsible to return data about a room, this is used
    to create a new room. The recipient is a write-only field so that
    it is not returned in the response. The recipient is the user that
    the sender wants to chat with.
    """

    recipient_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    recipient = SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "recipient_id", "recipient", "created_at")

    def create(self, validated_data: dict[str, int]) -> Room:
        recipient = validated_data.pop("recipient_id")
        sender = self.context["sender"]

        room = super().create(validated_data)
        RoomRecipient.objects.create(room=room, recipient=sender)
        RoomRecipient.objects.create(room=room, recipient=recipient)

        return room

    def get_recipient(self, room: Room) -> dict[str, str]:
        return UserSerializer(
            room.recipients.exclude(recipient=self.context["sender"])
            .first()
            .recipient
        ).data
