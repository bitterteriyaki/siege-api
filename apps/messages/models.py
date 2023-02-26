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

    sender = ForeignKey(User, on_delete=CASCADE, related_name="sent_messages")
    recipient = ForeignKey(
        User, on_delete=CASCADE, related_name="received_messages"
    )
    content = TextField(max_length=2048)
    # Whether the message has been deleted by the sender. We want to
    # keep the message in the database, but we don't want to show it
    # to the sender.
    is_deleted = BooleanField(default=True)

    class Meta:
        db_table = "messages"
