"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.urls import re_path

from apps.authentication.views import LoginView

app_name = "authentication"

urlpatterns = [
    re_path(r"^auth/login/?$", LoginView.as_view(), name="login"),
]
