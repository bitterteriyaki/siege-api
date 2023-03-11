"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any, cast

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from apps.rooms.logic.serializers import RoomSerializer
from apps.rooms.models import Room
from apps.users.models import User
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    RoomGenericViewSet = GenericViewSet[Room]
else:
    RoomGenericViewSet = GenericViewSet


class RoomsView(CreateModelMixin, RoomGenericViewSet):
    """This view is responsible for managing rooms."""

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = RoomSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kwargs["sender"] = cast(User, request.user)

        serializer = self.get_serializer(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)

        recipient = serializer.validated_data["recipient_id"]
        room = (
            Room.objects.filter(recipients__recipient=request.user)
            .filter(recipients__recipient=recipient)
            .first()
        )

        if room:
            return Response(
                self.get_serializer(room, context=kwargs).data,
                status=HTTP_200_OK,
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)
