"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.members.views import MembersView

app_name = "members"

urlpatterns = [
    re_path(
        r"^v1/guilds/(?P<guild_id>\d+)/members/?$",
        MembersView.as_view(),
        name="list",
    ),
]
