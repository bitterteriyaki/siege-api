"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.exceptions import NotFound

from apps.guilds.models import Guild


def get_guild(guild_id: int) -> Guild:
    """Get a guild by its ID. If the guild does not exist, raise a
    :class:`NotFound` exception.

    Parameters
    ----------
    guild_id: :class:`int`
        The ID of the guild to get.

    Returns
    -------
    :class:`Guild`
        The guild with the given ID.

    Raises
    ------
    :class:`NotFound`
        If the guild does not exist.
    """
    try:
        return Guild.objects.get(id=guild_id)
    except Guild.DoesNotExist as exc:
        raise NotFound("Guild not found.") from exc
