"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.models import DateTimeField, Model


class TimestampedModel(Model):
    """An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields. This is useful for tracking
    the creation and modification of objects. This model is intended
    to be inherited from, not used directly.
    """

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel`
        # should be ordered in reverse-chronological order. We can
        # override this on a per-model basis as needed, but
        # reverse-chronological is a good default ordering for most
        # models.
        ordering = ["-created_at", "-updated_at"]
