"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import CASCADE, CharField, ForeignKey

from apps.guilds.models import Guild
from core.models import TimestampedModel


class Channel(TimestampedModel):
    # The name of the channel.
    name = CharField(max_length=128)

    # The guild the channel belongs to.
    guild = ForeignKey(Guild, on_delete=CASCADE, related_name="channels")

    # The description of the channel. This is optional.
    description = CharField(max_length=256, null=True)
