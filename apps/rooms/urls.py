"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.rooms.views import RoomsView

app_name = "rooms"

router = SimpleRouter(trailing_slash=False)
router.register(r"rooms", RoomsView, basename="rooms")

urlpatterns = router.urls
