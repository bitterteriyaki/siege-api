"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from apps.guilds.logic.serializers import GuildSerializer
from apps.guilds.logic.utils import get_guild
from apps.guilds.models import Guild
from apps.members.models import Member
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    GuildView = RetrieveAPIView[Guild]
else:
    GuildView = RetrieveAPIView


class GuildsView(APIView):
    """View responsible for the `/guilds` route.

    Currently these are the endpoints available for this route:
    - `POST /guilds`: creates a new guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = GuildSerializer

    def post(self, request: Request) -> Response:
        context = {"request": request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        guild = serializer.save()

        member = Member(guild=guild, user=request.user)
        member.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class GuildRetrieveView(GuildView):
    """View responsible for the `/guilds/<guild_id>` route.

    Currently these are the endpoints available for this route:
    - `GET /guilds/<guild_id>`: retrieves a guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = GuildSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        guild_id = kwargs["guild_id"]
        serializer = self.serializer_class(get_guild(guild_id))

        return Response(serializer.data, status=HTTP_200_OK)
