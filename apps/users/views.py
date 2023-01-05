from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from apps.users.serializers import UsersSerializer
from core.renderers import UserJSONRenderer


class UsersView(APIView):
    """View responsible for the `/users` route.

    Currently these are the endpoints available for this route:
    - `POST /users`: creates a new user.
    """

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
