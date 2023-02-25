"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any

from rest_framework.exceptions import NotFound
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
)

from apps.messages.models import Message
from apps.users.logic.serializers import UserSerializer
from apps.users.logic.utils import get_user


class MessageSerializer(ModelSerializer[Message]):
    """This serializer is used to create a new message. It is used
    when the user is sending a message to another user.
    """

    content = CharField(max_length=2048)
    sender = SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = ("id", "content", "sender", "created_at")

    def create(self, validated_data: dict[str, str]) -> Message:
        sender = self.context["sender"]
        recipient = get_user(user_id=self.context["user_id"])

        if not recipient or not recipient.is_active:
            raise NotFound("User not found.")

        return Message.objects.create(
            sender=sender, recipient=recipient, **validated_data
        )

    def get_sender(self, message: Message) -> dict[str, Any]:
        return UserSerializer(message.sender).data
