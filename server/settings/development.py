"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from server.settings.base import *

# Here's a list of settings available in Django core and their default
# values.
# https://docs.djangoproject.com/en/4.1/ref/settings/#core-settings

DEBUG = True

# We can use any host name in development, so we set this to `*`.
# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts

ALLOWED_HOSTS = ["*"]


# In development, we don't need a secure password hasher. We can use
# MD5 instead, this is because we don't need to worry about security
# in development. However, we should use a secure password hasher in
# production, like PBKDF2 or Argon2.

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
