"""
Merged Django settings

- Keeps Django-CRM settings + your newer "core" project settings
- Uses env vars (.env) for secrets/DB/email where possible
- Preserves Django-CRM app/module settings (crm/common/tasks/voip + datetime_settings)
"""

import os
import sys
from pathlib import Path
from datetime import datetime as dt
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Load environment variables
load_dotenv()

# ---- Import modular settings from Django-CRM ---- #
from crm.settings import *          # NOQA
from common.settings import *       # NOQA
from tasks.settings import *        # NOQA
from voip.settings import *         # NOQA
from .datetime_settings import *    # NOQA

# ---- Django settings ---- #

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key-change-me")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Hosts / CSRF
ALLOWED_HOSTS = [
    "fastisha.com",
    "www.fastisha.com",
    "localhost",
    "127.0.0.1",
    "web",               # docker service name
    "38.242.150.81",
]

CSRF_TRUSTED_ORIGINS = [
    "https://fastisha.com",
    "https://www.fastisha.com",
]

FORMS_URLFIELD_ASSUME_HTTPS = True

# Database
# Prefer Postgres via env (your new settings). If not provided, fall back to SQLite.
POSTGRES_DBNAME = os.environ.get("POSTGRES_DBNAME", "").strip()
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME", "").strip()
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "").strip()

if POSTGRES_DBNAME and POSTGRES_USERNAME and POSTGRES_PASSWORD:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DBNAME,
            "USER": POSTGRES_USERNAME,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": os.environ.get("POSTGRES_HOST", "localhost").strip(),
            "PORT": os.environ.get("POSTGRES_PORT", "5432").strip(),
        }
    }
else:
    # Fallback (dev)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Email (merged: keep CRM defaults but allow env override)
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "crm@example.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX", "CRM: ")
SERVER_EMAIL = os.getenv("SERVER_EMAIL", "test@example.com")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", SERVER_EMAIL)

ADMINS = [("<Admin1>", "<admin1_box@example.com>")]

# Internationalization
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en")

LANGUAGES = [
    ("ar", "Arabic"),
    ("cs", "Czech"),
    ("de", "German"),
    ("el", "Greek"),
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("he", "Hebrew"),
    ("hi", "Hindi"),
    ("id", "Indonesian"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("nl", "Nederlands"),
    ("pl", "Polish"),
    ("pt-br", "Portuguese"),  # pt_BR
    ("ro", "Romanian"),
    ("ru", "Russian"),
    ("tr", "Turkish"),
    ("uk", "Ukrainian"),
    ("vi", "Vietnamese"),
    ("zh-hans", "Chinese"),
]

TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# URLs
LOGIN_URL = os.getenv("LOGIN_URL", "account_login")  # allauth default
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/dashboard")
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", "/")

# Application definition
INSTALLED_APPS = [
    # Django
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party (from core settings)
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "tailwind",
    "django_htmx",
    "crispy_forms",
    "crispy_tailwind",

    # Django-CRM apps
    "crm.apps.CrmConfig",
    "massmail.apps.MassmailConfig",
    "analytics.apps.AnalyticsConfig",
    "help",
    "tasks.apps.TasksConfig",
    "chat.apps.ChatConfig",
    "voip",
    "common.apps.CommonConfig",
    "settings",
    "quality",

    # Your local apps (from core settings)
    "apps.accounts",
    "apps.landing",
    "apps.dashboard",
    "apps.subscriptions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # From your core settings
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # CRM had LocaleMiddleware; keep it
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Your core additions
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",

    # CRM additions
    "common.utils.admin_redirect_middleware.AdminRedirectMiddleware",
    "common.utils.usermiddleware.UserMiddleware",
]

# NOTE:
# You must choose one ROOT_URLCONF/WSGI_APPLICATION project.
# Defaulting to your newer 'core' project.
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static / Media
STATIC_URL = "static/"

# Prefer production-ish config (whitenoise) but keep CRM's simple paths compatible.
STATIC_ROOT = os.getenv("STATIC_ROOT", str(BASE_DIR / "staticfiles"))
STATICFILES_DIRS = [str(BASE_DIR / "static")] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

FIXTURE_DIRS = ["tests/fixtures"]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

SITE_ID = int(os.getenv("SITE_ID", "1"))

# Security headers / HTTPS toggles
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower() == "true"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False").lower() == "true"
X_FRAME_OPTIONS = os.getenv("X_FRAME_OPTIONS", "SAMEORIGIN")

# ---- Django Allauth configuration ---- #
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_UNIQUE_EMAIL = True

# Tailwind configuration
TAILWIND_APP_NAME = "theme"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Stripe settings (from core settings)
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")

# ---- CRM settings ---- #

# For more security, replace the url prefixes with your own unique value.
SECRET_CRM_PREFIX = os.getenv("SECRET_CRM_PREFIX", "123/")
SECRET_ADMIN_PREFIX = os.getenv("SECRET_ADMIN_PREFIX", "456-admin/")
SECRET_LOGIN_PREFIX = os.getenv("SECRET_LOGIN_PREFIX", "789-login/")

CRM_IP = os.getenv("CRM_IP", "127.0.0.1")
CRM_REPLY_TO = [os.getenv("CRM_REPLY_TO", "'Do not reply' <crm@example.com>")]

NOT_ALLOWED_EMAILS = []

APP_ON_INDEX_PAGE = [
    "tasks", "crm", "analytics",
    "massmail", "common", "settings",
]

MODEL_ON_INDEX_PAGE = {
    "tasks": {"app_model_list": ["Task", "Memo"]},
    "crm": {"app_model_list": ["Request", "Deal", "Lead", "Company", "CrmEmail", "Payment", "Shipment"]},
    "analytics": {"app_model_list": ["IncomeStat", "RequestStat"]},
    "massmail": {"app_model_list": ["MailingOut", "EmlMessage"]},
    "common": {"app_model_list": ["UserProfile", "Reminder"]},
    "settings": {"app_model_list": ["PublicEmailDomain", "StopPhrase"]},
}

VAT = int(os.getenv("VAT", "0"))

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
OAUTH2_DATA = {
    "smtp.gmail.com": {
        "scope": "https://mail.google.com/",
        "accounts_base_url": "https://accounts.google.com",
        "auth_command": "o/oauth2/auth",
        "token_command": "o/oauth2/token",
    }
}
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "")

GOOGLE_RECAPTCHA_SITE_KEY = os.getenv("GOOGLE_RECAPTCHA_SITE_KEY", "")
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY", "")

GEOIP = os.getenv("GEOIP", "False").lower() == "true"
GEOIP_PATH = MEDIA_ROOT / "geodb"

SHOW_USER_CURRENT_TIME_ZONE = False
NO_NAME_STR = _("Untitled")

LOAD_EXCHANGE_RATE = os.getenv("LOAD_EXCHANGE_RATE", "False").lower() == "true"
LOADING_EXCHANGE_RATE_TIME = os.getenv("LOADING_EXCHANGE_RATE_TIME", "6:30")
LOAD_RATE_BACKEND = os.getenv("LOAD_RATE_BACKEND", "")

MARK_PAYMENTS_THROUGH_REP = os.getenv("MARK_PAYMENTS_THROUGH_REP", "False").lower() == "true"

SITE_TITLE = os.getenv("SITE_TITLE", "CRM")
ADMIN_HEADER = os.getenv("ADMIN_HEADER", "ADMIN")
ADMIN_TITLE = os.getenv("ADMIN_TITLE", "CRM Admin")
INDEX_TITLE = _("Main Menu")

MAILING = os.getenv("MAILING", "True").lower() == "true"

NAME_PREFIXES = [
    "Mr.", "Mrs.", "Ms.", "Miss", "Mx.", "Dr.", "Prof.", "Eng.", "Md.",
    "PhD", "Ph.D.", "Rev.", "Fr.", "Sr.", "Sra.", "Sir", "Lady", "Hon.",
    "Capt.", "Col.", "Lt.", "Maj.", "Gen.", "Judge", "Mister", "Mme.", "Mlle."
]

WEB_HELP = True

COPYRIGHT_STRING = f"Fastisha. Copyright (c) {dt.now().year}"
PROJECT_NAME = "Fastisha"
PROJECT_SITE = "https://djangocrm.github.io/info/"

# ---- Testing overrides ---- #
TESTING = sys.argv[1:2] == ["test"]
if TESTING:
    SECURE_SSL_REDIRECT = False
    LANGUAGE_CODE = "en"
    LANGUAGES = [("en", ""), ("uk", "")]
