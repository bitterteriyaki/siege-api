"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.users.views import UsersView

app_name = "users"

urlpatterns = [
    re_path("^v1/users/$", UsersView.as_view(), name="create"),
]
