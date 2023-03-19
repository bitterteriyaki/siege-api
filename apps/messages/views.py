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
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from apps.messages.logic.serializers import MessageSerializer
from apps.messages.models import Message
from apps.users.models import User
from core.renderers import BaseJSONRenderer
from core.websockets import pusher

if TYPE_CHECKING:
    MessageGenericViewSet = GenericViewSet[Message]
else:
    MessageGenericViewSet = GenericViewSet


class MessagesView(CreateModelMixin, MessageGenericViewSet):
    """This view is responsible for managing messages."""

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = MessageSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kwargs["sender"] = cast(User, request.user)

        serializer = self.get_serializer(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)

        message = serializer.save()
        pusher.trigger(f"room-{message.room.id}", "message", serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED)
