"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import CASCADE, CharField, ForeignKey

from apps.users.models import User
from core.models import TimestampedModel


class Guild(TimestampedModel):
    # The name of the guild. The name can be updated by members with
    # the permission to do so.
    name = CharField(max_length=128)

    # The owner of the guild. The owner is the only one who can
    # delete the guild. The owner can also transfer ownership to
    # another user.
    owner_id = ForeignKey(User, on_delete=CASCADE)

    # The description of the guild. This is optional. The description
    # can be updated by members with the permission to do so.
    description = CharField(max_length=255, blank=True, null=True)
