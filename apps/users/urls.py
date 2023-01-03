from django.urls import re_path

from apps.users.views import UsersView

app_name = "users"

urlpatterns = [
    re_path("^v1/users/$", UsersView.as_view(), name="create"),
]
