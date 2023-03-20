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

from apps.messages.logic.serializers import MessageSerializer
from apps.messages.models import Message
from apps.rooms.models import Room, RoomRecipient
from apps.users.models import User


class MessagesTestCase(APITestCase):
    """Test case responsible to test the messages endpoints."""

    def setUp(self) -> None:
        self.main_user = User.objects.create_user(
            username="main_user", email="main@email.com", password="password"
        )
        self.target_user = User.objects.create_user(
            username="target_user",
            email="target@email.com",
            password="password",
        )

        # Create a room between the main user and the target user.
        self.room = Room.objects.create()
        RoomRecipient.objects.create(room=self.room, recipient=self.main_user)
        RoomRecipient.objects.create(
            room=self.room, recipient=self.target_user
        )

    def test_send_message_successfully(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"room_id": self.room.id}
        )
        context = {"sender": self.main_user}

        res = self.client.post(url, {"content": "Hello world!"})
        message = Message.objects.get(room=self.room)

        expected = MessageSerializer(message, context=context).data

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertDictEqual(res.data, expected)

    def test_send_message_to_non_existing_room(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("messages:messages-list", kwargs={"room_id": 0})

        res = self.client.post(url, {"content": "Hello world!"})
        expected = {
            "status": HTTP_404_NOT_FOUND,
            "errors": {"detail": "Room not found"},
        }

        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)
        self.assertDictEqual(res.data, expected)

    def test_send_message_without_authentication(self) -> None:
        url = reverse(
            "messages:messages-list", kwargs={"room_id": self.room.id}
        )

        res = self.client.post(url, {"content": "Hello world!"})
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, 401)
        self.assertDictEqual(res.data, expected)

    def test_send_message_without_content(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"room_id": self.room.id}
        )

        res = self.client.post(url, {"content": ""})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"content": ["This field may not be blank"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_send_message_with_long_content(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"room_id": self.room.id}
        )

        res = self.client.post(url, {"content": "a" * 2049})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "content": [
                    "This field must have a maximum of 2048 characters"
                ]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_send_message_with_blank_content(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse(
            "messages:messages-list", kwargs={"room_id": self.room.id}
        )

        res = self.client.post(url, {"content": ""})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"content": ["This field may not be blank"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)
