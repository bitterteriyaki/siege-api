"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from apps.users.models import User


class AuthenticationTestCase(APITestCase):
    """Test cases for the authentication app."""

    def setUp(self):
        self.example = {"email": "user@email.com", "password": "password"}
        self.url = reverse("authentication:login")

        self.user = User.objects.create_user(
            **self.example,
            username="username",
        )

    def test_login_user_successfully(self):
        resp = self.client.post(self.url, self.example)

        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn("token", resp.data)
        self.assertEqual(resp.data["token"], self.user.token)

    def test_login_user_with_invalid_email(self):
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

    def test_login_user_with_wrong_password(self):
        self.example["password"] = "wrong_password"
        expected = "Unable to login with provided credentials."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("detail", details)
        self.assertIn(expected, details["detail"])

    def test_login_user_with_non_existent_email(self):
        self.example["email"] = "other@email.com"
        expected = "Unable to login with provided credentials."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("detail", details)
        self.assertIn(expected, details["detail"])

    def test_login_user_with_empty_email(self):
        self.example["email"] = ""
        expected = "This field may not be blank."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("email", details)
        self.assertIn(expected, details["email"])

    def test_login_user_with_empty_password(self):
        self.example["password"] = ""
        expected = "This field may not be blank."

        resp = self.client.post(self.url, self.example)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("password", details)
        self.assertIn(expected, details["password"])

    def test_login_user_with_missing_email(self):
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

    def test_login_user_with_missing_password(self):
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

    def test_login_user_null_email(self):
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

    def test_login_user_null_password(self):
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


class TokenAuthenticationTestCase(APITestCase):
    """Test case for the token authentication class."""

    def setUp(self):
        self.example = {
            "email": "user@email.com",
            "username": "user",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.example)

    def test_invalid_token_one_term(self):
        url = reverse("users:get", kwargs={"target": "me"})
        resp = self.client.get(url, HTTP_AUTHENTICATION="Token")

        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_invalid_token_three_terms(self):
        url = reverse("users:get", kwargs={"target": "me"})
        token = f"Token {self.user.token} another-term"

        resp = self.client.get(url, HTTP_AUTHENTICATION=token)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_invalid_token_wrong_prefix(self):
        url = reverse("users:get", kwargs={"target": "me"})
        token = f"Tokenn {self.user.token}"

        resp = self.client.get(url, HTTP_AUTHENTICATION=token)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)
