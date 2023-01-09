"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from server.settings.development import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# Application definition

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
}
