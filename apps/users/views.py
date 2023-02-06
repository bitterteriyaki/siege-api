"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Literal

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from apps.users.logic.serializers import SelfUserSerializer, UsersSerializer
from apps.users.models import User
from core.renderers import BaseJSONRenderer, UserJSONRenderer


class AuthenticatedRequest(Request):
    user: User


class SelfUserView(APIView):
    """View responsible for the `/users` route.

    Currently these are the endpoints available for this route:
    - `POST /users`: creates a new user.
    """

    permission_classes = (AllowAny,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = SelfUserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class UsersView(APIView):
    """View responsible for the `/users/<target>` route.

    Currently these are the endpoints available for this route:
    - `GET /users/<target>`: gets the user with the given ID.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer

    def get(
        self, request: AuthenticatedRequest, target: int | Literal["me"]
    ) -> Response:
        user = request.user if target == "me" else User.objects.get(id=target)
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=HTTP_200_OK)
