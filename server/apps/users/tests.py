from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APITestCase

from server.apps.users.models import User


class UsersTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("users:create")
        self.example = {
            "username": "user",
            "email": "user@email.com",
            "password": "password",
        }

    def test_create_user_sucessfully(self):
        resp = self.client.post(self.url, self.example)
        user = User.objects.get(email=self.example["email"])

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(resp.data["email"], user.email)
        self.assertEqual(resp.data["token"], user.token)

    def test_create_user_with_invalid_email(self):
        self.example["email"] = "invalid_email"

        resp = self.client.post(self.url, self.example)
        expected = "Enter a valid email address."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["email"][0], expected)

    def test_create_user_with_short_password(self):
        self.example["password"] = "abc"

        resp = self.client.post(self.url, self.example)
        expected = "Ensure this field has at least 8 characters."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["password"][0], expected)

    def test_create_user_with_long_password(self):
        self.example["password"] = "abc" * 100

        resp = self.client.post(self.url, self.example)
        expected = "Ensure this field has no more than 128 characters."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["password"][0], expected)

    def test_create_user_with_existing_email(self):
        self.client.post(self.url, self.example)

        resp = self.client.post(self.url, self.example)
        expected = "user with this email already exists."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["email"][0], expected)

    def test_create_user_with_long_email(self):
        self.example["email"] = "a" * 1000 + "@email.com"

        resp = self.client.post(self.url, self.example)
        expected = "Ensure this field has no more than 255 characters."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["email"][0], expected)

    def test_create_user_with_short_username(self):
        self.example["username"] = "a"

        resp = self.client.post(self.url, self.example)
        expected = "Ensure this field has at least 2 characters."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["username"][0], expected)

    def test_create_user_with_long_username(self):
        self.example["username"] = "a" * 100

        resp = self.client.post(self.url, self.example)
        expected = "Ensure this field has no more than 32 characters."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["username"][0], expected)

    def test_create_user_missing_email(self):
        del self.example["email"]

        resp = self.client.post(self.url, self.example)
        expected = "This field is required."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["email"][0], expected)

    def test_create_user_missing_password(self):
        del self.example["password"]

        resp = self.client.post(self.url, self.example)
        expected = "This field is required."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["password"][0], expected)

    def test_create_user_missing_username(self):
        del self.example["username"]

        resp = self.client.post(self.url, self.example)
        expected = "This field is required."

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["username"][0], expected)
