"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from rest_framework.routers import SimpleRouter

from apps.messages.views import MessagesView

app_name = "messages"

router = SimpleRouter(trailing_slash=False)
router.register(
    r"channels/(?P<user_id>[^./]+)/messages", MessagesView, basename="messages"
)

urlpatterns = router.urls
