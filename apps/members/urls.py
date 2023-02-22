"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.members.views import MembersViewSet

app_name = "members"

router = SimpleRouter(trailing_slash=False)
router.register(
    r"guilds/(?P<guild_id>[^/.]+)/members", MembersViewSet, basename="members"
)

urlpatterns = router.urls
