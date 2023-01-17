"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.apps import AppConfig

default_app_config = "apps.members.MembersConfig"


class MembersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.members"
