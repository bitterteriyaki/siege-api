"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from server.settings.development import *

# Here's a list of settings available in Django core and their default
# values.
# https://docs.djangoproject.com/en/4.1/ref/settings/#core-settings

# Since we are in a CI environment, we don't want to use the default
# database. PostgreSQL is too heavy for a CI environment, so we use
# SQLite instead.

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
}
