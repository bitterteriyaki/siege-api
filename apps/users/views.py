"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import TYPE_CHECKING, Any

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from apps.users.logic.serializers import SelfUserSerializer, UserSerializer
from apps.users.logic.utils import get_user
from apps.users.models import User
from core.renderers import BaseJSONRenderer

if TYPE_CHECKING:
    UserGenericViewSet = GenericViewSet[User]
else:
    UserGenericViewSet = GenericViewSet


class SelfUserView(CreateModelMixin, UserGenericViewSet):
    """This view is responsible for creating users. Since this viewset
    is supposed to be used for creating users, the used serializer will
    only contain the fields that ar e required for creating a user, and
    return the token of the created user.
    """

    permission_classes = [AllowAny]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = SelfUserSerializer


class UsersView(RetrieveModelMixin, UserGenericViewSet):
    """This view is responsible for retrieving users. Since this viewset
    is supposed to be used for retrieving users, the used serializer
    will only contain the fields that are required for retrieving a
    user, and return the user schema. It is required to be authenticated
    to use this view.
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        assert isinstance(request.user, User)

        pk = kwargs.pop("pk")
        # If the user is requesting their own data (/users/me), then
        # we will return the data of the authenticated user.
        target = request.user if pk == "me" else get_user(pk)

        serializer = self.serializer_class(target)
        return Response(serializer.data, status=HTTP_201_CREATED)
