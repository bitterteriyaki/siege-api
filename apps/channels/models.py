"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import CharField, ForeignKey, CASCADE

from core.models import TimestampedModel

from apps.guilds.models import Guild


class Channel(TimestampedModel):
    # The name of the channel.
    name = CharField(max_length=128)

    # The guild the channel belongs to.
    guild = ForeignKey(Guild, on_delete=CASCADE, related_name="channels")

    # The description of the channel. This is optional.
    description = CharField(max_length=255, blank=True, null=True)
