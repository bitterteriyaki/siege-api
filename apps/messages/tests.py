"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from apps.messages.logic.serialiazers import MessageSerializer
from apps.messages.models import Message
from apps.users.models import User


class MessagesTestCase(APITestCase):
    """Test case responsible to test the messages endpoints."""

    def setUp(self) -> None:
        self.main_user = User.objects.create_user(
            username="main_user",
            email="main@email.com",
            password="password",
        )
        self.target_user = User.objects.create_user(
            username="target_user",
            email="target@email.com",
            password="password",
        )

    def test_create_message_sucessfully(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"user_id": self.target_user.id}
        )

        res = self.client.post(url, {"content": "Hello World!"})
        message = Message.objects.get(content="Hello World!")

        expected = MessageSerializer(message).data

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertDictEqual(res.data, expected)

    def test_create_message_with_invalid_user(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("messages:messages-list", kwargs={"user_id": 3})
        res = self.client.post(url, {"content": "Hello World!"})

        expected = {
            "status": HTTP_404_NOT_FOUND,
            "errors": {"detail": "User not found"},
        }

        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)
        self.assertDictEqual(res.data, expected)

    def test_create_message_without_authentication(self) -> None:
        url = reverse(
            "messages:messages-list", kwargs={"user_id": self.target_user.id}
        )

        res = self.client.post(url, {"content": "Hello World!"})
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_create_message_send_to_self(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"user_id": self.main_user.id}
        )
        res = self.client.post(url, {"content": "Hello World!"})

        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"detail": "You cannot send a message to yourself"},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)
