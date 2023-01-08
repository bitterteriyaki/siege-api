"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path

urlpatterns = (
    # apps:
    re_path(r"^api/", include("apps.users.urls", namespace="users")),
    re_path(
        r"^api/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
)

if settings.DEBUG:
    urlpatterns += (
        # django-admin:
        re_path("^admin/", admin.site.urls),
    )
