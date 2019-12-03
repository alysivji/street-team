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
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") if IN_PRODUCTION else "zcj4**&#_&3cer3q)wf2a+^n-72p@l=b0#(m&!-n&4x#-+)hu("

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
    # internal
    "apps.common",
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
]

if not IN_PRODUCTION:
    INSTALLED_APPS.extend(["django_extensions", "django_pdb"])
    MIDDLEWARE.extend(["django_pdb.middleware.PdbMiddleware"])

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
                "apps.common.context_processors.from_settings",
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Custom Settings
TEST_RUNNER = "apps.common.runner.PytestTestRunner"
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
