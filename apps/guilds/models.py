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
    """ """

    name = CharField(max_length=126)
    owner_id = ForeignKey(User, on_delete=CASCADE)
    description = CharField(max_length=255, blank=True, null=True)
