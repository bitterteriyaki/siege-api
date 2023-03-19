"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APITestCase

from apps.rooms.logic.serializers import RoomSerializer
from apps.rooms.models import Room, RoomRecipient
from apps.users.models import User


class RoomsTestCase(APITestCase):
    """Test case responsible to test the rooms endpoints."""

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

    def test_create_room_sucessfully(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")
        context = {"sender": self.main_user}

        res = self.client.post(url, {"recipient": self.target_user.id})
        room = Room.objects.get(recipients__recipient=self.target_user)

        expected = RoomSerializer(room, context=context).data

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertDictEqual(res.data, expected)

    def test_create_already_existing_room(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")
        context = {"sender": self.main_user}

        room = Room.objects.create()
        RoomRecipient.objects.create(room=room, recipient=self.main_user)
        RoomRecipient.objects.create(room=room, recipient=self.target_user)

        res = self.client.post(url, {"recipient": self.target_user.id})
        expected = RoomSerializer(room, context=context).data

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertDictEqual(res.data, expected)

    def test_create_room_without_authentication(self) -> None:
        url = reverse("rooms:rooms-list")

        res = self.client.post(url, {"recipient": self.target_user.id})
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_create_room_with_invalid_recipient_id(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")

        res = self.client.post(url, {"recipient": 0})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"recipient": ["User not found"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_room_with_self_recipient(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")

        res = self.client.post(url, {"recipient": self.main_user.id})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "recipient": ["You cannot send a message to this user"]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_room_with_no_recipient(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")

        res = self.client.post(url, {})
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"recipient": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_room_has_member(self) -> None:
        self.client.force_authenticate(user=self.main_user)

        url = reverse("rooms:rooms-list")
        context = {"sender": self.main_user}

        res = self.client.post(url, {"recipient": self.target_user.id})
        room = Room.objects.get(recipients__recipient=self.target_user)

        expected = RoomSerializer(room, context=context).data

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertDictEqual(res.data, expected)

        self.assertTrue(room.has_member(user=self.main_user))
        self.assertTrue(room.has_member(user=self.target_user))

        # Test with a user that is not a member of the room.
        user = User.objects.create_user(
            email="some@user.com", password="password", username="some_user"
        )
        self.assertFalse(room.has_member(user=user))
