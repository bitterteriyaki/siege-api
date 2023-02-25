"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import CASCADE, BooleanField, ForeignKey, TextField

from apps.users.models import User
from core.models import TimestampedModel


class Message(TimestampedModel):
    """Represents a message sent by a user to another user."""

    # The user who sent the message.
    sender = ForeignKey(User, on_delete=CASCADE, related_name="sent_messages")

    # The user who received the message.
    recipient = ForeignKey(
        User, on_delete=CASCADE, related_name="received_messages"
    )

    # The content of the message.
    content = TextField(max_length=2048)

    # Whether the message has been deleted by the sender.
    is_deleted = BooleanField(default=True)

    class Meta:
        # The name of the table in the database.
        db_table = "messages"
