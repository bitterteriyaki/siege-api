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

from apps.authentication.logic.serializers import LoginSerializer
from core.renderers import BaseJSONRenderer


class LoginView(APIView):
    """This view is responsible for authenticating users. It is not
    required to be authenticated to use this view. The view will
    return a token that can be used to authenticate the user in
    future requests.
    """

    permission_classes = [AllowAny]
    renderer_classes = [BaseJSONRenderer]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=HTTP_200_OK)
