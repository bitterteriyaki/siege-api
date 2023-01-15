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
    ManyToManyField,
    Model,
)

from apps.users.models import User
from core.models import TimestampedModel


class Guild(TimestampedModel):
    # The name of the guild. The name can be updated by members with
    # the permission to do so.
    name = CharField(max_length=128)

    # The owner of the guild. The owner is the only one who can
    # delete the guild. The owner can also transfer ownership to
    # another user.
    owner_id = ForeignKey(User, on_delete=CASCADE, related_name="owned_guilds")

    # The description of the guild. This is optional. The description
    # can be updated by members with the permission to do so.
    description = CharField(max_length=255, blank=True, null=True)

    # The members of the guild. This is a many-to-many relationship
    # between the guild and the users. The members can be updated by
    # members with the permission to do so.
    members = ManyToManyField(
        User, through="GuildMember", related_name="guilds"
    )


class GuildMember(Model):
    # The user who is a member of the guild.
    user = ForeignKey(User, on_delete=CASCADE)

    # The guild that the user is a member of.
    guild = ForeignKey(Guild, on_delete=CASCADE)

    # The nickname of the user in the guild. This is optional. The
    # nickname can be updated by members with the permission to do
    # so. The nickname must have a maximum length of 32 characters.
    nick = CharField(max_length=32, blank=True, null=True)

    # The date and time when the user joined the guild.
    joined_at = DateTimeField(auto_now_add=True)

    class Meta:
        # The name of the table in the database.
        db_table = "guilds_members"
