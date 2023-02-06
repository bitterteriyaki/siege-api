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
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from apps.users.logic.backend import (
    encode_to_b64,
    generate_token,
    validate_token,
)
from apps.users.models import User


class AuthenticationTestCase(APITestCase):
    """Test cases for `/auth` route."""

    def setUp(self) -> None:
        self.example = {"email": "user@email.com", "password": "password"}
        self.url = reverse("authentication:login")

        self.user = User.objects.create_user(
            **self.example,
            username="username",
        )

    def test_login_user_successfully(self) -> None:
        resp = self.client.post(self.url, self.example)

        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn("token", resp.data)
        self.assertEqual(resp.data["token"], self.user.token)

    def test_login_user_with_invalid_email(self) -> None:
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

    def test_login_user_with_wrong_password(self) -> None:
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

    def test_login_user_with_non_existent_email(self) -> None:
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

    def test_login_user_with_empty_email(self) -> None:
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

    def test_login_user_with_empty_password(self) -> None:
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

    def test_login_user_with_missing_email(self) -> None:
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

    def test_login_user_with_missing_password(self) -> None:
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

    def test_login_user_null_email(self) -> None:
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

    def test_login_user_null_password(self) -> None:
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

    def setUp(self) -> None:
        self.example = {
            "email": "user@email.com",
            "username": "user",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.example)

    def test_valid_token_v1(self) -> None:
        validated = validate_token(self.user.token)
        expected = (self.user, self.user.token)
        self.assertTupleEqual(validated, expected)

    def test_invalid_token_v1_one_term_wrong_version(self) -> None:
        self.assertRaises(ValidationError, validate_token, "invalid-token")

    def test_invalid_token_v1_many_terms_wrong_version(self) -> None:
        token = "invalid.token.format.here"
        self.assertRaises(ValidationError, validate_token, token)

    def test_invalid_token_v1_one_term_correct_version(self) -> None:
        self.assertRaises(ValidationError, validate_token, "v1.invalid-token")

    def test_invalid_token_v1_many_terms_correct_version(self) -> None:
        token = "v1.invalid.token.format.here"
        self.assertRaises(ValidationError, validate_token, token)

    def test_invalid_token_v1_invalid_user_id(self) -> None:
        token = "v1.test.invalid-token"
        self.assertRaises(ValidationError, validate_token, token)

    def test_invalid_token_v1_invalid_user(self) -> None:
        user_id = encode_to_b64(str(self.user.id + 1).encode("utf-8"))
        token = f"v1.{user_id}.invalid-token"
        self.assertRaises(ValidationError, validate_token, token)

    def test_invalid_token_v1_invalid_signature(self) -> None:
        user_id = encode_to_b64(str(self.user.id).encode("utf-8"))
        token = f"v1.{user_id}.invalid-token"
        self.assertRaises(ValidationError, validate_token, token)

    def test_invalid_token_v1_wrong_signature(self) -> None:
        email = "another@email.com"
        token = generate_token(str(self.user.id), email, self.user.password)
        self.assertRaises(ValidationError, validate_token, token)
