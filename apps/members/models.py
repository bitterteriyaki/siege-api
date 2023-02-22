"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
)

from apps.guilds.models import Guild
from apps.users.models import User


class Member(Model):
    # The user who is a member of the guild.
    user = ForeignKey(User, on_delete=CASCADE)

    # The guild that the user is a member of.
    guild = ForeignKey(Guild, on_delete=CASCADE)

    # The nickname of the user in the guild. This is optional. The
    # nickname must have a maximum length of 32 characters.
    nick = CharField(max_length=32, null=True)

    # The date and time when the user joined the guild.
    joined_at = DateTimeField(auto_now_add=True)
