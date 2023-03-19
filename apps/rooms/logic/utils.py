"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound

from apps.rooms.models import Room


def get_room(room_id: int) -> Room:
    """Get a room by is ID. If the room does no exist raise a
    :class:`NotFound` exception.

    Parameters
    ----------
    room_id: :class:`int`
        The ID of the room to get.

    Returns
    -------
    :class:`Room`
        The room with the given ID.

    Raises
    ------
    :class:`NotFound`
        If the room does not exist.
    """
    try:
        return Room.objects.get(id=room_id)
    except Room.DoesNotExist as exc:
        raise NotFound(_("Room not found.")) from exc
