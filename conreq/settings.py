"""
Django settings for Conreq project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import json
import os
import secrets

from django.core.management.utils import get_random_secret_key

from conreq.core import log

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Helper Functions
def get_bool_from_env(name, default_value):
    env_var = os.environ.get(name)
    if isinstance(env_var, str):
        if env_var.lower() == "true":
            return True
        if env_var.lower() == "false":
            return False
    return default_value


# Environment Variables
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("DEBUG", True)
DB_ENGINE = os.environ.get("DB_ENGINE", "")
MYSQL_CONFIG_FILE = os.environ.get("MYSQL_CONFIG_FILE", "")
USE_ROLLING_SECRET_KEY = get_bool_from_env("USE_ROLLING_SECRET_KEY", False)
USE_SSL = get_bool_from_env("USE_SSL", False)
DATA_DIR = os.environ.get("DATA_DIR")

# Logging
log.configure(log.get_logger(), log.INFO)
if DEBUG:
    log.console_stream(log.get_logger(), log.WARNING)


# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not DATA_DIR:
    DATA_DIR = BASE_DIR


# Security Settings
if USE_ROLLING_SECRET_KEY:
    SECRET_KEY = get_random_secret_key()  # Key used for cryptographic signing

ALLOWED_HOSTS = ["*"]
SECURE_BROWSER_XSS_FILTER = (
    True  # Sets "X-XSS-Protection: 1; mode=block" header on all responses
)

if USE_SSL:
    SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
    SECURE_HSTS_PRELOAD = True  # Allow for HSTS preload
    SECURE_HSTS_SECONDS = 31536000  # Allow for HSTS preload
    SESSION_COOKIE_SECURE = True  # Only send cookie over HTTPS
    CSRF_USE_SESSIONS = True  # Store CSRF token within session cookie
    CSRF_COOKIE_SECURE = True  # Only send cookie over HTTPS
    CSRF_COOKIE_HTTPONLY = True  # Do not allow JS to access cookie
    LANGUAGE_COOKIE_SECURE = True  # Only send cookie over HTTPS
    LANGUAGE_COOKIE_HTTPONLY = True  # Do not allow JS to access cookie


# Encryption Keys
conreq_settings_file = os.path.join(DATA_DIR, "settings.json")
file_update_needed = False

# Create the file if it doesn't exist
if not os.path.exists(conreq_settings_file):
    with open(conreq_settings_file, "w") as file:
        file.write("{}")

# Read the file
with open(conreq_settings_file, "r+") as file:
    config_file = json.load(file)

    # Obtain the DB Encryption Key from the file
    if (
        config_file.__contains__("DB_ENCRYPTION_KEY")
        and config_file["DB_ENCRYPTION_KEY"] is not None
        and config_file["DB_ENCRYPTION_KEY"] != ""
    ):
        FIELD_ENCRYPTION_KEYS = [config_file["DB_ENCRYPTION_KEY"]]

    # DB Encryption Key wasn't found, a new one is needed
    else:
        FIELD_ENCRYPTION_KEYS = [secrets.token_hex(32)]
        config_file["DB_ENCRYPTION_KEY"] = FIELD_ENCRYPTION_KEYS[0]
        file_update_needed = True

    # Obtain the Secret Key from the file
    if (
        config_file.__contains__("SECRET_KEY")
        and config_file["SECRET_KEY"] is not None
        and config_file["SECRET_KEY"] != ""
        and not USE_ROLLING_SECRET_KEY
    ):
        SECRET_KEY = config_file["SECRET_KEY"]

    # Secret Key wasn't found, a new one is needed
    elif not USE_ROLLING_SECRET_KEY:
        SECRET_KEY = get_random_secret_key()
        config_file["SECRET_KEY"] = SECRET_KEY
        file_update_needed = True

# Save the new file if needed
if file_update_needed:
    with open(conreq_settings_file, "w") as file:
        print("Updating settings.json to ", config_file)
        file.write(json.dumps(config_file))


# Application Settings
HTML_MINIFY = True
DJVERSION_GIT_USE_COMMIT = True
DJVERSION_GIT_REPO_PATH = BASE_DIR


# Application Definitions
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "conreq.apps.homepage",
    "conreq.apps.discover",
    "conreq.apps.more_info",
    "conreq.apps.search",
    "conreq.apps.server_settings",
    "channels",  # Websocket library
    "encrypted_fields",  # Allow for encrypted text in the DB
    "solo",  # Allow for single-row fields in the DB
    "django_cleanup.apps.CleanupConfig",  # Automatically delete old image files
    "djversion",  # Obtains the git commit as a version number
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files on Daphne securely
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",  # Compresses HTML files
    "htmlmin.middleware.MarkRequestMiddleware",  # Marks the request as minified
]


# Caching Database
CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": os.path.join(DATA_DIR, "cache"),
        "TIMEOUT": 300,  # Django setting for default timeout of each key.
        "SHARDS": 8,  # Number of db files to create
        "DATABASE_TIMEOUT": 0.010,  # 10 milliseconds
        "OPTIONS": {"size_limit": 2 ** 30},  # 1 gigabyte
    }
}


# URL Routing and Page Rendering
ROOT_URLCONF = "conreq.urls"
ASGI_APPLICATION = "conreq.asgi.application"

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
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if DB_ENGINE.upper() == "MYSQL" and MYSQL_CONFIG_FILE != "":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "OPTIONS": {
                "read_default_file": MYSQL_CONFIG_FILE,
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(DATA_DIR, "db.sqlite3"),
            "OPTIONS": {
                "timeout": 30,
            },
        }
    }


# Password Validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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

LOGIN_REDIRECT_URL = "homepage:index"
LOGIN_URL = "signin"


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static Files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static-deploy")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
