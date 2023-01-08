"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from server.settings.base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

DEBUG = False


# Application definition

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
