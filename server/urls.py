"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import include, path, re_path

urlpatterns = (
    # apps:
    path("", include("apps.users.urls", namespace="users")),
    path("", include("apps.guilds.urls", namespace="guilds")),
    path("", include("apps.authentication.urls", namespace="authentication")),
    path("", include("apps.members.urls", namespace="members")),
    re_path(r"^api/", include("apps.channels.urls", namespace="channels")),
)
