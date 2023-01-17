"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from apps.guilds.logic.serializers import GuildSerializer
from apps.guilds.models import Guild
from apps.members.models import Member
from core.renderers import BaseJSONRenderer


class GuildsView(APIView):
    """View responsible for the `/guilds` route.

    Currently these are the endpoints available for this route:
    - `POST /guilds`: creates a new guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = GuildSerializer

    def post(self, request):
        context = {"request": request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        guild = serializer.save()

        member = Member(guild=guild, user=request.user)
        member.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class GuildRetrieveView(RetrieveAPIView):
    """View responsible for the `/guilds/<guild_id>` route.

    Currently these are the endpoints available for this route:
    - `GET /guilds/<guild_id>`: retrieves a guild.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = GuildSerializer

    def get(self, request, guild_id):
        try:
            guild = Guild.objects.get(id=guild_id)
        except Guild.DoesNotExist as exc:
            raise NotFound("Guild not found.") from exc
        else:
            serializer = self.serializer_class(guild)
            return Response(serializer.data, status=HTTP_200_OK)
