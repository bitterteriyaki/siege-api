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

from apps.guilds.logic.serializers import GuildSerializer
from apps.guilds.models import Guild
from apps.users.models import User


class GuildsTestCase(APITestCase):
    """Test case responsible to test the guild management endpoints."""

    def setUp(self) -> None:
        credentials = {
            "username": "user",
            "password": "password",
            "email": "user@email.com",
        }

        self.user = User.objects.create_user(**credentials)

    def test_create_guild_sucessfully(self) -> None:
        url = reverse("guilds:guilds-list")
        self.client.force_authenticate(user=self.user)

        data = {"name": "guild", "description": "description"}
        res = self.client.post(url, data=data)

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertIn("id", res.data)

        guild = Guild.objects.get(id=res.data["id"])
        expected = GuildSerializer(guild)

        self.assertDictEqual(res.data, expected.data)

    def test_create_guild_without_authentication(self) -> None:
        url = reverse("guilds:guilds-list")

        data = {"name": "guild", "description": "description"}
        res = self.client.post(url, data=data)

        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_create_guild_without_name(self) -> None:
        url = reverse("guilds:guilds-list")
        self.client.force_authenticate(user=self.user)

        data = {"description": "description"}
        res = self.client.post(url, data=data)

        expected = {
            "status": HTTP_400_BAD_REQUEST,
            "errors": {"name": ["This field is required"]},
        }

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, expected)

    def test_get_guild_sucessfully(self) -> None:
        self.client.force_authenticate(user=self.user)

        guild = Guild.objects.create(
            name="guild", description="description", owner_id=self.user
        )
        url = reverse("guilds:guilds-detail", kwargs={"pk": guild.id})

        res = self.client.get(url)
        expected = GuildSerializer(guild)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertDictEqual(res.data, expected.data)

    def test_get_guild_without_authentication(self) -> None:
        guild = Guild.objects.create(
            name="guild", description="description", owner_id=self.user
        )
        url = reverse("guilds:guilds-detail", kwargs={"pk": guild.id})

        res = self.client.get(url)

        expected = {
            "status": HTTP_401_UNAUTHORIZED,
            "errors": {
                "detail": "Authentication credentials were not provided"
            },
        }

        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(res.data, expected)

    def test_get_non_existing_guild(self) -> None:
        url = reverse("guilds:guilds-detail", kwargs={"pk": 1})
        self.client.force_authenticate(user=self.user)

        res = self.client.get(url)
        expected = {
            "status": HTTP_404_NOT_FOUND,
            "errors": {"detail": "Not found"},
        }

        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)
        self.assertDictEqual(res.data, expected)
