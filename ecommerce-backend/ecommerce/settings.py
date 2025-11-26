"""Django settings for the e‑commerce project.

This configuration module centralizes all settings required for the
application. It heavily relies on environment variables to allow
configuration to vary between environments (development, staging,
production) without modifying source code. Sensitive data such as
secret keys and API credentials should be supplied via the environment
or a secrets manager rather than committed to version control.
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv


# Determine the base directory two levels above this file so that
# relative paths can be constructed easily.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from ``.env`` in the project root if it
# exists. This allows developers to define local overrides without
# polluting version control.
env_path = BASE_DIR / ".." / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-default-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes"}

hosts = os.getenv("ALLOWED_HOSTS")
if hosts:
    ALLOWED_HOSTS = [h.strip() for h in hosts.split(",") if h.strip()]
else:
    # Safe defaults for local development
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third‑party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "django_celery_results",
    "django_celery_beat",

    # Project apps (use AppConfig classes to ensure signals are imported)
    "users.apps.UsersConfig",
    "catalog.apps.CatalogConfig",
    "payments.apps.PaymentsConfig",
    "orders.apps.OrdersConfig",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware defined in core.middleware
    "core.middleware.RequestTimingMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "ecommerce.wsgi.application"
ASGI_APPLICATION = "ecommerce.asgi.application"


# Database configuration. By default the project uses SQLite for
# convenience. To use PostgreSQL or another database engine, set
# ``DB_ENGINE`` and the corresponding connection credentials in your
# environment.
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", ""),
        "PORT": os.environ.get("DB_PORT", ""),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization. The default time zone is configurable via
# ``TZ`` environment variable. For this project we default to Africa/Nairobi.
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TZ", "Africa/Nairobi")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# REST framework configuration. These defaults enforce JWT
# authentication and pagination for all API endpoints.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# drf-spectacular configuration for OpenAPI/Swagger
SPECTACULAR_SETTINGS = {
    "TITLE": "E‑Commerce API",
    "DESCRIPTION": "Backend for product catalog, categories, orders, payments and user management",
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# Cache configuration using django‑redis. This improves performance for
# session and query caching. If ``REDIS_URL`` is not set, an in‑memory
# backend will be used.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Use cache based sessions for performance
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Celery configuration
CELERY_BROKER_URL = os.environ.get("RABBITMQ_URL") or os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Store task results using django-celery-results
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"

CELERY_BEAT_SCHEDULE = {
    "disable-out-of-stock-products": {
        "task": "core.tasks.disable_out_of_stock_products",
        "schedule": 3600.0,
    },
}

if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = "memory://"



# Miscellaneous configuration
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"