"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.guilds.views import GuildsView

app_name = "guilds"

router = SimpleRouter(trailing_slash=False)
router.register(r"guilds", GuildsView, basename="guilds")

urlpatterns = router.urls
