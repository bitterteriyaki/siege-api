"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any

from django.db.models import CASCADE, ForeignKey

from apps.users.models import User
from core.models import TimestampedModel


class Room(TimestampedModel):
    """Represents a room."""

    # Remove Mypy complaints about missing attributes.
    # These attributes are added by the `related_name` argument.
    recipients: Any

    class Meta:
        db_table = "rooms"


class RoomRecipient(TimestampedModel):
    """Represents a recipient of a room."""

    room = ForeignKey(Room, on_delete=CASCADE, related_name="recipients")
    recipient = ForeignKey(User, on_delete=CASCADE, related_name="rooms")

    class Meta:
        db_table = "room_recipients"
