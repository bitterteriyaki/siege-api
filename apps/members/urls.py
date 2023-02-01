"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import DefaultRouter

from apps.members.views import MembersViewSet

app_name = "members"

router = DefaultRouter()
router.register(
    r"v1/guilds/(?P<guild_id>\d+)/members", MembersViewSet, basename="members"
)

urlpatterns = router.urls
