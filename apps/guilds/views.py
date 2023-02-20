"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any, cast

from django.utils.translation import gettext as _
from guardian.shortcuts import assign_perm
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from apps.guilds.logic.serializers import GuildSerializer
from apps.guilds.models import Guild
from apps.users.models import User
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    GuildGenericViewSet = GenericViewSet[Guild]
else:
    GuildGenericViewSet = GenericViewSet


class GuildsView(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GuildGenericViewSet,
):
    """This view is responsible for managing guilds. It is required to
    be authenticated to use this view. Some actions are also restricted
    to the guild owner -- such as deleting the guild, but superusers
    can perform any action.
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = GuildSerializer
    queryset = Guild.objects.all()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = cast(User, request.user)
        guild = serializer.save()

        # Assign the permission to delete the guild to the user.
        assign_perm("delete_guild", user, guild)

        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = cast(User, request.user)
        guild = self.get_object()

        if not user.has_perm("guilds.delete_guild", guild):
            raise PermissionDenied(
                _("You do not have permission to perform this action.")
            )

        return super().destroy(request, *args, **kwargs)
