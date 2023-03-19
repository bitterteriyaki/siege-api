"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any

from rest_framework.exceptions import NotFound
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APITestCase

from apps.users.logic.serializers import UserSerializer
from apps.users.logic.utils import get_user
from apps.users.models import User


class SelfUserTestCase(APITestCase):
    """Test case responsible to test the user creation endpoint."""

    def setUp(self) -> None:
        self.url = reverse("users:self-list")
        self.example: dict[str, Any] = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }

    def test_create_user_sucessfully(self) -> None:
        res = self.client.post(self.url, self.example)
        user = User.objects.get(email=self.example["email"])

        expected = {"token": user.token}

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_invalid_email(self) -> None:
        self.example["email"] = "invalid_email"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["Invalid e-mail address"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_short_password(self) -> None:
        self.example["password"] = "abc"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "password": ["This field must have at least 8 characters"]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_long_password(self) -> None:
        self.example["password"] = "abc" * 100

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "password": [
                    "This field must have a maximum of 128 characters"
                ]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_short_username(self) -> None:
        self.example["username"] = "a"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "username": ["This field must have at least 2 characters"]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_long_username(self) -> None:
        self.example["username"] = "abc" * 100

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "username": ["This field must have a maximum of 32 characters"]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_existing(self) -> None:
        self.client.post(self.url, self.example)

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["E-mail already in use"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_long_email(self) -> None:
        self.example["email"] = "a" * 1000 + "@email.com"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "email": ["This field must have a maximum of 256 characters"]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_missing_email(self) -> None:
        del self.example["email"]

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_missing_password(self) -> None:
        del self.example["password"]

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"password": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_missing_username(self) -> None:
        del self.example["username"]

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"username": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_null_username(self) -> None:
        self.example["username"] = None

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"username": ["This field may not be null"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_null_email(self) -> None:
        self.example["email"] = None

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["This field may not be null"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_null_password(self) -> None:
        self.example["password"] = None

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"password": ["This field may not be null"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_create_user_with_no_available_tags(self) -> None:
        # Seed the database with 9.999 users with the same tag
        for i in range(1, 10_000):
            self.example["email"] = f"user{i}@email.com"

            user = User(**self.example, tag=i)
            user.save()

        self.example["email"] = "another.user@email.com"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {
                "username": [
                    "Too many users have this username, please try another"
                ]
            },
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)


class UsersTestCase(APITestCase):
    """Test case for users retrieving endpoints."""

    def setUp(self) -> None:
        self.example = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.example)

    def test_get_self(self) -> None:
        url = reverse("users:users-detail", kwargs={"pk": "me"})
        self.client.force_authenticate(self.user)

        res = self.client.get(url)
        expected = UserSerializer(self.user)

        self.assertDictEqual(res.data, expected.data)

    def test_get_self_without_authentication(self) -> None:
        url = reverse("users:users-detail", kwargs={"pk": "me"})

        res = self.client.get(url)
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_get_user(self) -> None:
        url = reverse("users:users-detail", kwargs={"pk": self.user.id})
        self.client.force_authenticate(self.user)

        res = self.client.get(url)
        expected = UserSerializer(self.user)

        self.assertDictEqual(res.data, expected.data)

    def test_utils_get_user(self) -> None:
        self.assertEqual(get_user(self.user.id), self.user)

    def test_utils_get_user_with_invalid_id(self) -> None:
        self.assertRaises(NotFound, get_user, 0)

    def test_get_user_without_authentication(self) -> None:
        url = reverse("users:users-detail", kwargs={"pk": self.user.id})

        res = self.client.get(url)
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)
