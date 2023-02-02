"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.channels.views import ChannelsView

app_name = "channels"

urlpatterns = [
    re_path(r"^v1/guilds/(?P<guild_id>\d+)/channels/?$", ChannelsView.as_view(), name="create"),
]
