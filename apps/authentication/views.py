"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.authentication.logic.serializers import AuthenticationSerializer
from core.renderers import BaseJSONRenderer


class LoginView(APIView):
    """View responsible for the `/auth/login` route.

    Currently these are the endpoints available for this route:
    - `POST /auth/login`: authenticates a user.
    """

    permission_classes = (AllowAny,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = AuthenticationSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=HTTP_200_OK)
