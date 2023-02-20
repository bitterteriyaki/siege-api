"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import CASCADE, CharField, ForeignKey, ManyToManyField

from apps.users.models import User
from core.models import TimestampedModel


class Guild(TimestampedModel):
    # Every guild has a unique ID that is used to identify them in the
    # database. In this case, we are just telling Mypy that the type
    # of the `id` field is an integer.
    id: int

    # The name of the guild.
    name = CharField(max_length=128)

    # The owner of the guild. The owner is the only one who can
    # delete the guild. The owner can also transfer ownership to
    # another user.
    owner_id = ForeignKey(User, on_delete=CASCADE, related_name="owned_guilds")

    # The description of the guild. This is optional.
    description = CharField(max_length=256, blank=True, null=True)

    # The members of the guild. This is a many-to-many relationship
    # between the guild and the users.
    members = ManyToManyField(
        User, through="members.Member", related_name="guilds"
    )
