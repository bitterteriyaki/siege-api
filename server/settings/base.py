"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from os.path import join

from server.settings import BASE_DIR, config

# Here's a list of settings available in Django core and their default
# values.
# https://docs.djangoproject.com/en/4.1/ref/settings/#core-settings

SECRET_KEY = config("DJANGO_SECRET_KEY")

# We don't want to append a slash to the end of URLs, so we disable it.
# This is because we want to use the same URLs schema for both the API
# and the front-end.

APPEND_SLASH = False

INSTALLED_APPS = [
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Third-party apps:
    "rest_framework",
    # Local apps:
    "apps.users",
    "apps.authentication",
    "apps.guilds",
    "apps.members",
    "apps.channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

WSGI_APPLICATION = "server.wsgi.application"

# A nested dictionary whose contents map a database alias to a
# dictionary containing the options for an individual database.
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("DJANGO_DATABASE_HOST"),
        "PORT": config("DJANGO_DATABASE_PORT", cast=int),
        "CONN_MAX_AGE": config("CONN_MAX_AGE", cast=int, default=60),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}

# The list of validators that are used to check the strength of user's
# passwords. See Password validation for more details.
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

BASE_VALIDATOR = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{BASE_VALIDATOR}.UserAttributeSimilarityValidator"},
    {"NAME": f"{BASE_VALIDATOR}.MinimumLengthValidator"},
    {"NAME": f"{BASE_VALIDATOR}.CommonPasswordValidator"},
    {"NAME": f"{BASE_VALIDATOR}.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [join(BASE_DIR, "locale")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The model to use to represent a `User`.
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"


# Django Rest Framework settings
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "core.exceptions.main_exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "core.renderers.BaseJSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.authentication.logic.backend.TokenAuthentication",
    ],
}
