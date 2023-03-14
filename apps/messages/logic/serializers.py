"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
)

from apps.messages.models import Message
from apps.rooms.logic.utils import get_room
from apps.users.logic.serializers import UserSerializer


class MessageSerializer(ModelSerializer[Message]):
    """This serializer is responsible for serializing messages."""

    content = CharField(max_length=2048)
    sender = SerializerMethodField()

    class Meta:
        model = Message
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "content", "sender", "created_at")

    def create(self, validated_data: dict[str, str]) -> Message:
        sender = self.context["sender"]
        room = get_room(room_id=self.context["room_id"])

        if not room.has_member(user=sender):
            raise PermissionDenied(
                {"detail": _("You cannot send messages to this room.")}
            )

        return Message.objects.create(
            **validated_data, sender=sender, room=room
        )

    def get_sender(self, message: Message) -> dict[str, str]:
        return UserSerializer(message.sender).data
