"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from apps.channels.logic.serializers import ChannelSerializer
from apps.channels.models import Channel
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    ChannelGenericViewSet = GenericViewSet[Channel]
else:
    ChannelGenericViewSet = GenericViewSet


class ChannelsView(CreateModelMixin, ChannelGenericViewSet):
    """This view is responsible for creating channels. It is needed to
    be authenticated to use this view.
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = ChannelSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)
