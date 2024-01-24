"""
Django settings for api project.
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
print(f"api/settings.py > ENVIRONMENT: {ENVIRONMENT}")

IN_DEV = ENVIRONMENT == "development"
IN_STAGING = ENVIRONMENT == "staging"
IN_PROD = ENVIRONMENT == "production"


def _env_get_required(setting_name):
    """Get the value of an environment"""
    setting = os.environ.get(setting_name, "")
    if not IN_DEV:
        assert setting not in {
            None,
            "",
        }, "{0} must be defined as an environment variable".format(setting_name)
    return setting


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "unfold",  # Unfold Admin panel
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    # "import_export",
    # "drf_spectacular",
    # Internal apps
    "common",
    "core",
    "todos",
    # "properties",
    # "projects",
    # "notifications",
    # "messaging",
]


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)  # Front End

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    # "https://{URL}.vercel.app",
    # "https://{URL}.com",
    # "https://www.{URL}.com",
    # "https://stripe.com", # Stripe
    # "https://*.up.railway.app", # Railway
    # "https://{URL}-*.up.railway.app", # Railway
    # "https://*.s3.amazonaws.com", # S3 Bucket
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    # "https://{URL}.herokuapp.com",
    # "https://*.stripe.com",
    # "https://{URL}.vercel.app",
    # "https://{URL}.com",
    # "https://www.{URL}.com",
    # "https://*.up.railway.app",
    # "https://{URL}-api-*.up.railway.app",
    # "https://*.s3.amazonaws.com",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "api.urls"

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

ASGI_APPLICATION = "api.asgi.application"
WSGI_APPLICATION = "api.wsgi.application"

#
# Django Rest Framework Configuration
#
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.PageNumberPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated"),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "ALLOWED_VERSIONS": [
        "1.0",
    ],
    "DEFAULT_VERSION": "1.0",
    "PAGE_SIZE": 10,
}

# DRF Simple JWT Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "JTI_CLAIM": "jti",
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    # this is the default serializer
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # this is the custom serializer
    "TOKEN_OBTAIN_SERIALIZER": "core.serializers.UserLoginSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
}

REST_USE_JWT = True  # to use JSON web tokens

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

default_db = dj_database_url.config()
print(f"default_db => {default_db}")

if bool(default_db):
    DATABASES = {"default": default_db}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": _env_get_required("DB_NAME"),
            "USER": _env_get_required("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": _env_get_required("DB_HOST"),
            "PORT": _env_get_required("DB_PORT"),
            "CONN_MAX_AGE": os.environ.get("DB_CONN_MAX_AGE", 820),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "core.CustomUser"
# LOGIN_URL="/auth/login"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = "static/"
# STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CURRENT_DOMAIN = os.environ.get("CURRENT_DOMAIN")
CURRENT_PORT = os.environ.get("CURRENT_PORT")


#
# Email settings
#
# Mailgun Configuration
# if USE_CUSTOM_SMTP is true, Mailgun settings will be used
# otherwise, emails will show in the terminal. This is useful for local development

USE_CUSTOM_SMTP = os.environ.get("USE_CUSTOM_SMTP")
if USE_CUSTOM_SMTP == "True":
    EMAIL_HOST = _env_get_required("SMTP_HOST")
    EMAIL_PORT = os.environ.get("SMTP_PORT", 587)
    EMAIL_HOST_USER = _env_get_required("SMTP_USER")
    EMAIL_HOST_PASSWORD = _env_get_required("SMTP_PASSWORD")
    EMAIL_ALLOWED_DOMAINS = _env_get_required("SMTP_VALID_TESTING_DOMAINS")
    EMAIL_USE_TLS = True
    MAILGUN_WEBHOOK_SIGNING_KEY = _env_get_required("MAILGUN_WEBHOOK_SIGNING_KEY")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Admin User""", "test@example.com")]  # update
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# Django Storages - S3 config WIP
# USE_AWS_STORAGE = os.environ.get("USE_AWS_STORAGE") == "True"
# PRIVATE_MEDIAFILES_LOCATION = ""
# AWS_ACCESS_KEY_ID = ""
# AWS_SECRET_ACCESS_KEY = ""
# AWS_STORAGE_BUCKET_NAME = ""
# AWS_S3_CUSTOM_DOMAIN = ""
# AWS_S3_REGION_NAME = ""
# AWS_DEFAULT_ACL = None

# STATICFILES_DIRS = [
#     # os.path.join(BASE_DIR, "static/"),
# ]

# DRF Spectacular Swagger generator
SPECTACULAR_SETTINGS = {
    "TITLE": "Matt Django Boilerplate API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    # available SwaggerUI versions: https://github.com/swagger-api/swagger-ui/releases
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.35.1",  # default
    "SWAGGER_UI_FAVICON_HREF": STATIC_URL
    + "your_company_favicon.png",  # default is swagger favicon
}


# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e. 2.5 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # i.e. 100 MB


#
# HTTPS Everywhere outside the dev environment
#
if not IN_DEV:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    MIDDLEWARE += ["django.middleware.security.SecurityMiddleware"]
