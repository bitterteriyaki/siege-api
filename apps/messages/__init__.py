"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.apps import AppConfig

default_app_config = "apps.messages.MessagesConfig"


class MessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.messages"
