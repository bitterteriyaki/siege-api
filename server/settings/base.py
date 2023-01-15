"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from pathlib import Path

from server.settings import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = config("DJANGO_SECRET_KEY")


# Application definition

INSTALLED_APPS = (
    # default django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # third-party apps:
    "rest_framework",
    # local apps:
    "apps.users",
    "apps.authentication",
    "apps.guilds",
)

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

# Database
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
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

BASE_VALIDATOR = "django.contrib.auth.password_validation"

SIMILARITY_VALIDATOR = f"{BASE_VALIDATOR}.UserAttributeSimilarityValidator"
MINIMUM_LENGTH_VALIDATOR = f"{BASE_VALIDATOR}.MinimumLengthValidator"
COMMON_PASSWORD_VALIDATOR = f"{BASE_VALIDATOR}.CommonPasswordValidator"
NUMERIC_PASSWORD_VALIDATOR = f"{BASE_VALIDATOR}.NumericPasswordValidator"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": SIMILARITY_VALIDATOR,
    },
    {
        "NAME": MINIMUM_LENGTH_VALIDATOR,
    },
    {
        "NAME": COMMON_PASSWORD_VALIDATOR,
    },
    {
        "NAME": NUMERIC_PASSWORD_VALIDATOR,
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tell Django about the custom `User` model we created.
AUTH_USER_MODEL = "users.User"

# Django Rest Framework settings
# https://www.django-rest-framework.org/api-guide/settings/

DEFAULT_VERSIONING_CLASS = "rest_framework.versioning.URLPathVersioning"

TEST_REQUEST_DEFAULT_FORMAT = "json"

EXCEPTION_HANDLER = "core.exceptions.main_exception_handler"

DEFAULT_RENDERER_CLASSES = ("core.renderers.BaseJSONRenderer",)

DEFAULT_AUTHENTICATION_CLASSES = (
    "apps.authentication.logic.backend.TokenAuthentication",
)

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": DEFAULT_VERSIONING_CLASS,
    "TEST_REQUEST_DEFAULT_FORMAT": TEST_REQUEST_DEFAULT_FORMAT,
    "EXCEPTION_HANDLER": EXCEPTION_HANDLER,
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
}
