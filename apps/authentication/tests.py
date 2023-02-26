"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from typing import Any

from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIRequestFactory, APITestCase

from apps.authentication.logic.backend import TokenAuthentication
from apps.users.models import User


class LoginTestCase(APITestCase):
    """Test case for the login endpoint."""

    def setUp(self) -> None:
        self.example: dict[str, Any] = {
            "email": "user@email.com",
            "password": "password",
        }
        self.url = reverse("authentication:login")
        self.user = User.objects.create_user(
            **self.example, username="username"
        )

    def test_login_user_successfully(self) -> None:
        res = self.client.post(self.url, self.example)
        expected = {"token": self.user.token}

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_invalid_email(self) -> None:
        self.example["email"] = "invalid_email"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["Invalid e-mail address"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_wrong_password(self) -> None:
        self.example["password"] = "wrong_password"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {"detail": "Unable to login with provided credentials"},
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_non_existent_email(self) -> None:
        self.example["email"] = "other@email.com"

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {"detail": "Unable to login with provided credentials"},
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_empty_email(self) -> None:
        self.example["email"] = ""

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["This field may not be blank"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_empty_password(self) -> None:
        self.example["password"] = ""

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"password": ["This field may not be blank"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_missing_email(self) -> None:
        del self.example["email"]

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_missing_password(self) -> None:
        del self.example["password"]

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"password": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_null_email(self) -> None:
        self.example["email"] = None

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"email": ["This field may not be null"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_login_user_with_null_password(self) -> None:
        self.example["password"] = None

        res = self.client.post(self.url, self.example)
        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"password": ["This field may not be null"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)


class TokenAuthenticationTestCase(APITestCase):
    """Test case for the token authentication."""

    def setUp(self) -> None:
        self.auth = TokenAuthentication()
        self.user = User.objects.create_user(
            email="user@email.com",
            username="username",
            password="password",
        )
        self.url = reverse("authentication:login")
        self.factory = APIRequestFactory()
        self.payload = {"email": self.user.email, "password": "password"}

    def test_authenticate_with_valid_token(self) -> None:
        res = self.auth.validate_token(self.user.token)
        expected = (self.user, self.user.token)

        self.assertTupleEqual(res, expected)

    def test_authenticate_with_invalid_token(self) -> None:
        self.assertRaises(
            ValidationError, self.auth.validate_token, "invalid_token"
        )

    def test_authenticate_with_non_existing_user(self) -> None:
        user = User(
            id=2,
            email="user@email.com",
            username="username",
            password="password",
        )
        self.assertRaises(
            ValidationError, self.auth.validate_token, user.token
        )

    def test_authenticate_with_no_header(self) -> None:
        req = self.factory.get(self.url, self.payload)
        self.assertIsNone(self.auth.authenticate(req))

    def test_authenticate_with_short_header(self) -> None:
        req = self.factory.get(
            self.url, self.payload, HTTP_AUTHORIZATION="Token"
        )
        self.assertIsNone(self.auth.authenticate(req))

    def test_authenticate_with_long_header(self) -> None:
        req = self.factory.get(
            self.url, self.payload, HTTP_AUTHORIZATION="Token invalid token"
        )
        self.assertIsNone(self.auth.authenticate(req))

    def test_authenticate_with_invalid_header_prefix(self) -> None:
        req = self.factory.get(
            self.url, self.payload, HTTP_AUTHORIZATION="Invalid invalid_token"
        )
        self.assertIsNone(self.auth.authenticate(req))

    def test_authenticate_with_valid_header(self) -> None:
        req = self.factory.get(
            self.url,
            self.payload,
            HTTP_AUTHORIZATION=f"Token {self.user.token}",
        )

        res = self.auth.authenticate(req)
        expected = (self.user, self.user.token)

        assert res is not None
        self.assertTupleEqual(res, expected)
