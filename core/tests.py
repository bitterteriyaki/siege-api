"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView

from core.exceptions import main_exception_handler


class CoreTestCase(APITestCase):
    """Test case responsible to test core functionalities."""

    def test_internal_server_error(self) -> None:
        factory = APIRequestFactory()
        exc = IntegrityError()

        payload = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }

        context = {
            "view": APIView(),
            "args": (),
            "kwargs": {},
            "request": factory.post("/users", payload, format="json"),
        }

        self.assertIsNone(main_exception_handler(exc, context))
