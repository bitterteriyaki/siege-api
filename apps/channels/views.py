"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from apps.channels.logic.serializers import ChannelSerializer
from core.renderers import BaseJSONRenderer


class ChannelsView(APIView):
    """View responsible for the `/channels` route.

    Currently these are the endpoints available for this route:
    - `POST /channels`: creates a new channel.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = ChannelSerializer

    def post(self, request, guild_id):
        context = {"guild_id": guild_id}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
