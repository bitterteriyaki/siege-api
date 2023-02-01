"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.guilds.logic.utils import get_guild
from apps.members.logic.serializers import MemberSerializer
from core.renderers import BaseJSONRenderer


class MembersViewSet(ReadOnlyModelViewSet):
    """Viewset responsible for the `/guilds/<guild_id>/members` route.
    This route is used to retrieve all members of a guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = MemberSerializer

    def get_queryset(self):
        guild = get_guild(self.kwargs["guild_id"])
        return guild.member_set.all()
