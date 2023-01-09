"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import include, re_path

auth = "authentication"

urlpatterns = (
    # apps:
    re_path(r"^api/", include("apps.users.urls", namespace="users")),
    re_path(r"^api/", include(f"apps.{auth}.urls", namespace=auth)),
)
