"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import include, re_path

urlpatterns = (
    # apps:
    re_path(r"^api/", include("apps.users.urls", namespace="users")),
    re_path(
        r"^api/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
    re_path(r"^api/", include("apps.guilds.urls", namespace="guilds")),
    re_path(r"^api/", include("apps.members.urls", namespace="members")),
)
