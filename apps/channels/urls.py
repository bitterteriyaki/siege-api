"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.channels.views import ChannelsView

app_name = "channels"

router = SimpleRouter(trailing_slash=False)
router.register(
    r"guilds/(?P<guild_id>[^/.]+)/channels", ChannelsView, basename="channels"
)

urlpatterns = router.urls
