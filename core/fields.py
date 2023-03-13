"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework.relations import RelatedField

from apps.rooms.models import Room
from apps.users.logic.serializers import UserSerializer
from apps.users.models import User

if TYPE_CHECKING:
    RelatedFieldBase = RelatedField[Room, User, Any]
else:
    RelatedFieldBase = RelatedField


class FetchUserField(RelatedFieldBase):
    """This field is responsible for fetching a user by its primary key.
    The returned value is a rendered user object. This field is used
    to create a new room.
    """

    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _("User not found."),
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["source"] = "*"
        super().__init__(*args, **kwargs)

    def use_pk_only_optimization(self) -> bool:
        return True

    def to_internal_value(self, data: Any) -> Any:
        queryset = self.get_queryset()

        try:
            return {"recipient": queryset.get(pk=data)}
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data)

    def to_representation(self, room: Room) -> dict[str, str]:
        return UserSerializer(
            room.recipients.exclude(recipient=self.context["sender"])
            .first()
            .recipient
        ).data
