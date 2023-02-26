"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import include, path

urlpatterns = (
    # apps:
    path("", include("apps.users.urls", namespace="users")),
    path("", include("apps.authentication.urls", namespace="authentication")),
    path("", include("apps.messages.urls", namespace="messages")),
)
