"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.members.logic.serializers import MemberSerializer
from apps.members.models import Member
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    MemberGenericViewSet = ReadOnlyModelViewSet[Member]
else:
    MemberGenericViewSet = ReadOnlyModelViewSet


class MembersViewSet(MemberGenericViewSet):
    """This view is responsible for managing members. It is required to
    be authenticated to use this view. Currently, this view only
    supports listing and retrieving members.
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = MemberSerializer

    def get_queryset(self) -> Any:
        return Member.objects.filter(guild_id=self.kwargs["guild_id"])
