"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.guilds.models import Guild
from apps.members.logic.serializers import MemberSerializer
from core.renderers import BaseJSONRenderer


class MembersView(APIView):
    """View responsible for the `/guilds/<guild_id>/members` route.

    Currently these are the endpoints available for this route:
    - `GET /guilds/<guild_id>/members`: retrieves all members of a
      guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = MemberSerializer

    def get(self, request, guild_id):
        try:
            guild = Guild.objects.get(id=guild_id)
        except Guild.DoesNotExist as exc:
            raise NotFound("Guild not found.") from exc
        else:
            serializer = self.serializer_class(
                guild.member_set.all(), many=True
            )
            return Response(serializer.data, status=HTTP_200_OK)
