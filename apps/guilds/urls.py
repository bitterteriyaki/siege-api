"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.guilds.views import GuildRetrieveView, GuildsView

app_name = "guilds"

urlpatterns = [
    re_path(r"^v1/guilds/?$", GuildsView.as_view(), name="create"),
    re_path(
        r"^v1/guilds/(?P<guild_id>\d+|me)/?",
        GuildRetrieveView.as_view(),
        name="get",
    ),
]
