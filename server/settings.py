"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-up5#(s^m02$$iqsw5fl@jmeikgr*v(bnyr(8+m42m$(hxohj^t"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.users",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # this is temporary, until we add a dotenv file
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "database",
        "PORT": 5432,
    }
}

# NOTE:
# This is a temporary solution to allow the tests to run on
# GitHub Actions. It is necessary to add a way to separate the
# environments later on.

if os.getenv("GITHUB_WORKFLOW"):
    DATABASES["default"]["NAME"] = "github-actions"
    DATABASES["default"]["HOST"] = "localhost"


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

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
DEFAULT_RENDERER_CLASSES = [
    "core.renderers.BaseJSONRenderer",
]

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": DEFAULT_VERSIONING_CLASS,
    "TEST_REQUEST_DEFAULT_FORMAT": TEST_REQUEST_DEFAULT_FORMAT,
    "EXCEPTION_HANDLER": EXCEPTION_HANDLER,
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
}
