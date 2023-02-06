"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APITestCase

from apps.users.models import User


class SelfUserTestCase(APITestCase):
    """Test cases for `/users` route."""

    def setUp(self) -> None:
        self.url = reverse("users:create")
        self.example = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }

    def setup_seeding(self) -> None:
        for i in range(1, 10_000):
            self.example["email"] = f"user{i}@email.com"
            User.objects.create_user(**self.example, tag=i)

    def test_create_user_sucessfully(self) -> None:
        resp = self.client.post(self.url, self.example)
        user = User.objects.get(email=self.example["email"])

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(resp.data["token"], user.token)

    def test_create_user_with_invalid_email(self) -> None:
        self.example["email"] = "invalid_email"
        expected = "Enter a valid email address."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_create_user_with_short_password(self) -> None:
        self.example["password"] = "abc"
        expected = "Ensure this field has at least 8 characters."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("password", details)
        self.assertIn(expected, details["password"])

    def test_create_user_with_long_password(self) -> None:
        self.example["password"] = "abc" * 100
        expected = "Ensure this field has no more than 128 characters."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("password", details)
        self.assertIn(expected, details["password"])

    def test_create_user_with_existing_email(self) -> None:
        self.client.post(self.url, self.example)
        expected = "This email is already in use."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_create_user_with_long_email(self) -> None:
        self.example["email"] = "a" * 1000 + "@email.com"
        expected = "Ensure this field has no more than 255 characters."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_create_user_with_short_username(self) -> None:
        self.example["username"] = "a"
        expected = "Ensure this field has at least 2 characters."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("username", details)
        self.assertIn(expected, details["username"])

    def test_create_user_with_long_username(self) -> None:
        self.example["username"] = "a" * 100
        expected = "Ensure this field has no more than 32 characters."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("username", details)
        self.assertIn(expected, details["username"])

    def test_create_user_missing_email(self) -> None:
        del self.example["email"]
        expected = "This field is required."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_create_user_missing_password(self) -> None:
        del self.example["password"]
        expected = "This field is required."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("password", details)
        self.assertIn(expected, details["password"])

    def test_create_user_missing_username(self) -> None:
        del self.example["username"]
        expected = "This field is required."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("username", details)
        self.assertIn(expected, details["username"])

    def test_create_user_with_null_username(self) -> None:
        self.example["username"] = None
        expected = "This field may not be null."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("username", details)
        self.assertIn(expected, details["username"])

    def test_create_user_with_null_email(self) -> None:
        self.example["email"] = None
        expected = "This field may not be null."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_create_user_with_null_password(self) -> None:
        self.example["password"] = None
        expected = "This field may not be null."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("password", details)
        self.assertIn(expected, details["password"])

    def test_create_user_no_available_tags(self) -> None:
        self.setup_seeding()
        self.example["email"] = "another.user@email.com"
        expected = "No available tags."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn(expected, details)

    def test_create_user_with_existing_tag(self) -> None:
        User.objects.create_user(**self.example, tag=1)
        self.assertRaises(
            ValidationError, User.objects.create_user, **self.example, tag=1
        )


class UsersTestCase(APITestCase):
    """Test cases for `/users/<user_id>` route."""

    def setUp(self) -> None:
        self.example = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.example)

    def test_get_self(self) -> None:
        url = reverse("users:get", kwargs={"target": "me"})
        self.client.force_authenticate(self.user)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTTP_200_OK)

        self.assertIn("id", resp.data)
        self.assertIn("username", resp.data)
        self.assertIn("tag", resp.data)

        self.assertEqual(resp.data["id"], self.user.id)
        self.assertEqual(resp.data["username"], self.user.username)
        self.assertEqual(resp.data["tag"], f"{self.user.tag:04}")

    def test_get_user(self) -> None:
        self.example["email"] = "another.user@email.com"
        another_user = User.objects.create_user(**self.example)

        url = reverse("users:get", kwargs={"target": another_user.id})
        self.client.force_authenticate(self.user)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTTP_200_OK)

        self.assertIn("id", resp.data)
        self.assertIn("username", resp.data)
        self.assertIn("tag", resp.data)

        self.assertEqual(resp.data["id"], another_user.id)
        self.assertEqual(resp.data["username"], another_user.username)
        self.assertEqual(resp.data["tag"], f"{another_user.tag:04}")
