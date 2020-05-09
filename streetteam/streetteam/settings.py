"""
Django settings for streetteam project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# User defined vars
IN_PRODUCTION = os.getenv("IN_PRODUCTION") == "1"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") if IN_PRODUCTION else "zcj4**&#_&3cer3q)wf2a+^n-72p@l=b0#(m&!-n&4x#-+)hu("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if IN_PRODUCTION else True

ALLOWED_HOSTS = ["0.0.0.0", ".sivji.com"] if IN_PRODUCTION else ["0.0.0.0", ".ngrok.io"]
APPEND_SLASH = True

# set in traefik
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if IN_PRODUCTION else None

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "rest_framework",  # REST APIs
    "watchman",  # status endpoints for services (db, cache, storage, etc)
    "social_django",  # login using oauth providers
    "django_fsm",  # declarative state management for django models
    "django_fsm_log",  # audit log for django fsm changes
    "admin_honeypot",  # fake Django Admin login screen to capture unauthorized access
    # internal
    "apps.debug",
    "apps.mediahub",
    "apps.twilio_integration",
    "apps.users",
    "apps.website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # needs to be after security
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.SuperuserCanViewDebugToolbarInProductionMiddleware",
]

if DEBUG:
    INSTALLED_APPS.extend(["django_extensions", "django_pdb", "debug_toolbar"])
    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
    MIDDLEWARE.extend(["django_pdb.middleware.PdbMiddleware"])

    # tricks to have debug toolbar when developing with docker
    # https://stackoverflow.com/questions/26898597/django-debug-toolbar-and-docker
    INTERNAL_IPS = ["0.0.0.0"]
    import socket

    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

ROOT_URLCONF = "streetteam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.from_settings",
            ]
        },
    }
]

WSGI_APPLICATION = "streetteam.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# development environment setting
DATABASES = {}
DATABASES["default"] = dj_database_url.config(env="DB_URI")


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Authentication backends
# https://docs.djangoproject.com/en/2.2/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = ["social_core.backends.github.GithubOAuth2", "django.contrib.auth.backends.ModelBackend"]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static and Media Files are stored on a Blob Store and served via http
# LocalStack for localdev
# DigitalOcean Blob Store with a CDN for staging and production
# Using django-storages to upload files to CDN
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_ENDPOINT_URL = "http://localstack:4566"  # env var
AWS_ACCESS_KEY_ID = "foo"  # env var
AWS_SECRET_ACCESS_KEY = "bar"  # env var
AWS_STORAGE_BUCKET_NAME = "streetteam"  # env var
AWS_DEFAULT_ACL = "public-read"

STATIC_URL = "http://localstack:4566/"  # env var
MEDIA_URL = "http://localstack:4566/"  # env var


# Custom Settings
TEST_RUNNER = "common.runner.PytestTestRunner"
AUTH_USER_MODEL = "users.User"


# Watchman -- monitoring Django services
# https://github.com/mwarkentin/django-watchman
WATCHMAN_CHECKS = ("watchman.checks.caches", "watchman.checks.databases")
WATCHMAN_AUTH_DECORATOR = "django.contrib.admin.views.decorators.staff_member_required"


# Python Social Auth -- login using OAuth providers
# https://python-social-auth.readthedocs.io/
# https://python-social-auth.readthedocs.io/en/latest/backends/github.html
LOGIN_URL = "/"
SOCIAL_AUTH_PASSWORDLESS = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/account"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/error"  # TODO
SOCIAL_AUTH_LOGOUT_REDIRECT_URL = "/"
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
SOCIAL_AUTH_GITHUB_KEY = os.getenv("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SOCIAL_AUTH_GITHUB_SCOPE = ["read:user", "user:email"]


# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "random_token")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "random_token")
TWILIO_SERVICE_SID = os.getenv("TWILIO_SERVICE_SID", "random_token")
