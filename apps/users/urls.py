"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.users.views import SelfUserView, UsersView

app_name = "users"

router = SimpleRouter(trailing_slash=False)
router.register(r"users", SelfUserView, basename="self")
router.register(r"users", UsersView, basename="users")

urlpatterns = router.urls
