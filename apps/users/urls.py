"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.users.views import SelfUserView, UsersView

app_name = "users"

urlpatterns = [
    re_path(r"^v1/users/?$", SelfUserView.as_view(), name="create"),
    re_path(
        r"^v1/users/(?P<target>\d+|me)/?$", UsersView.as_view(), name="get"
    ),
]
