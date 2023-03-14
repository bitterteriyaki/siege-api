"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any, cast

from django.db.models import CASCADE, ForeignKey

from apps.users.models import User
from core.models import TimestampedModel


class Room(TimestampedModel):
    """Represents a room."""

    # Telling Mypy that the type of this field is an integer.
    # This is necessary because Mypy doesn't know that Django will
    # automatically add an `id` field to the model.
    id: int

    # Remove Mypy complaints about missing attributes.
    # These attributes are added by the `related_name` argument.
    recipients: Any

    class Meta:
        db_table = "rooms"

    def has_member(self, *, user: User) -> bool:
        """Check if a user is a member of the room.

        Parameters
        ----------
        user: :class:`User`
            The user to check.

        Returns
        -------
        :class:`bool`
            Whether the user is a member of the room.
        """
        return cast(bool, self.recipients.filter(recipient=user).exists())


class RoomRecipient(TimestampedModel):
    """Represents a recipient of a room."""

    room = ForeignKey(Room, on_delete=CASCADE, related_name="recipients")
    recipient = ForeignKey(User, on_delete=CASCADE, related_name="rooms")

    class Meta:
        db_table = "room_recipients"
