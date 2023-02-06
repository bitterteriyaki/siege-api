"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from apps.users.models import User


class GuildsTestCase(APITestCase):
    """Test cases for `/guilds` route."""

    def setUp(self) -> None:
        credentials = {
            "username": "user",
            "password": "password",
            "email": "user@email.com",
        }

        self.user = User.objects.create_user(**credentials)

    def test_create_guild_sucessfully(self) -> None:
        url = reverse("guilds:create")
        self.client.force_authenticate(user=self.user)

        data = {"name": "guild", "description": "description"}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertIn("id", resp.data)
        self.assertIn("name", resp.data)
        self.assertIn("description", resp.data)
        self.assertIn("owner_id", resp.data)

        self.assertEqual(resp.data["name"], data["name"])
        self.assertEqual(resp.data["description"], data["description"])
        self.assertEqual(resp.data["owner_id"], self.user.id)

    def test_create_guild_without_authentication(self) -> None:
        url = reverse("guilds:create")
        expected = "Authentication credentials were not provided."

        data = {"name": "guild", "description": "description"}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("detail", details)
        self.assertIn(expected, details["detail"])

    def test_create_guild_without_name(self) -> None:
        url = reverse("guilds:create")
        expected = "This field is required."

        self.client.force_authenticate(user=self.user)

        data = {"description": "description"}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("name", details)
        self.assertIn(expected, details["name"])

    def test_get_guild_sucessfully(self) -> None:
        url = reverse("guilds:create")
        self.client.force_authenticate(user=self.user)

        data = {"name": "guild", "description": "description"}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertIn("id", resp.data)

        guild_id = resp.data["id"]
        url = reverse("guilds:get", kwargs={"guild_id": guild_id})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn("id", resp.data)
        self.assertIn("name", resp.data)
        self.assertIn("description", resp.data)
        self.assertIn("owner_id", resp.data)

        self.assertEqual(resp.data["name"], data["name"])
        self.assertEqual(resp.data["description"], data["description"])
        self.assertEqual(resp.data["owner_id"], self.user.id)

    def test_get_non_existing_guild(self) -> None:
        url = reverse("guilds:get", kwargs={"guild_id": 1})
        self.client.force_authenticate(user=self.user)

        expected = "Guild not found."
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)
        self.assertIn("error", resp.data)

        error = resp.data["error"]
        self.assertIn("details", error)

        details = error["details"]
        self.assertIn("detail", details)
        self.assertIn(expected, details["detail"])
