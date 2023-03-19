"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from pusher import Pusher

from server.settings import config

pusher = Pusher(
    app_id=config("PUSHER_APP_ID"),
    key=config("PUSHER_KEY"),
    secret=config("PUSHER_SECRET"),
    cluster=config("PUSHER_CLUSTER"),
    ssl=True,
)
